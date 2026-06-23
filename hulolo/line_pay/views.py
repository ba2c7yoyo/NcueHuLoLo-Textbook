'''
此檔案是處理 LINE Pay 付款流程的 API 介面，
為第 11 章的程式碼，目的為提供程式碼複製與讀者參考，詳情如書籍內容，
換句話說，這個頁面就算啟動網站後，仍無法直接使用，
需搭配前端串接及安裝 Django-REST-framework 才能完成付款流程建置。
'''

# 程式碼 11-2
import uuid
import hmac
import hashlib
import base64

# 程式碼 11-4
import os
import json
import requests
import random
from django.utils import timezone, dateformat
from rest_framework.views import APIView
from rest_framework.response import Response

# 程式碼 11-17
import re
from .models import Order

# 程式碼 11-5
channel_id = os.getenv("LINE_PAY_CHANNEL_ID")
channel_secret = os.getenv("LINE_PAY_CHANNEL_SECRET")
base_url = os.getenv("LINE_PAY_API_BASE")

# 程式碼 11-3
def generate_linepay_headers(
        request_body: str,
        channel_id: str,
        channel_secret: str,
        request_uri: str,
    ): 	 # <-有個好可愛的哭臉
    nonce = str(uuid.uuid4())

    message = f"{channel_secret}{request_uri}{request_body}{nonce}"
    message_bytes = message.encode("utf-8")
    secret_bytes = channel_secret.encode("utf-8")

    digest = hmac.new(secret_bytes, message_bytes, hashlib.sha256).digest()
    signature = base64.b64encode(digest).decode()

    return {
        "Content-Type": "application/json",
        "X-LINE-ChannelId": channel_id,
        "X-LINE-Authorization-Nonce": nonce,
        "X-LINE-Authorization": signature,
    }

# 程式碼 11-7
# 程式碼 11-8
class PayView(APIView):
    def post(self, request):
        api_path = "/v4/payments/request"
        request_api_url = f"{base_url}{api_path}"
        # 從前端取得商品 ID 與數量
        product_id = request.data.get("productId")
        product_quantity = int(request.data.get("productQuantity"))
        # 定義商品資料，實務上會改成從資料庫查詢
        product_map = {
            "kapybara-keychain-01": {
                "name": "【限量款】卡皮巴拉春季鑰匙圈",
                "unit_price": 30,
                "image_url": "https://example.com/kapy-keychain-01.png",
            }
        }
        product = product_map.get(product_id)
        if not product:
            return Response(
                {"detail": "product not found"},  status=404,
            )
        product_unit_price = product["unit_price"]
        total_amount = product_unit_price * product_quantity
        
        # 程式碼 11-8
        # 接續在 total_amount 變數之下
        # 年月日時分秒，如 20280619120323
        timestamp = dateformat.format(
            timezone.now() + timezone.timedelta(hours=8),
            "YmdHis",
        )
        # 三位隨機數，範圍 000~999
        random_suffix = f"{random.randint(0, 999):03d}"  

        # 組合成訂單編號，如：OD_20280619120323001
        order_id = f"OD_{timestamp}{random_suffix}"

        # 程式碼 11-9
        # 接續在 order_id 變數之下
        request_body = {
            "amount": total_amount,
            "currency": "TWD",
            "orderId": order_id, # 訂單編號
            "packages": [
                {
                    "id": product_id, # 商品 ID
                    "amount": total_amount, # 所有商品總價
                    "products": [
                        {
                            "name": product["name"], # 商品名稱
                            "imageUrl": product["image_url"], # 商品圖片
                            "quantity": product_quantity, # 商品數量
                            "price": product_unit_price, # 商品單價
                        },
                    ],
                },
            ],
            "options": {
                "display": {"locale": "zh_TW"},
            },
            "redirectUrls": {
                "confirmUrl": "https://example.tw/line-pay/confirm/",
                "cancelUrl": "https://example.tw/line-pay/cancel/",
            },
        }

        # 將 request body 轉成 JSON 字串
        request_body_json = json.dumps(request_body, separators=(",", ":"))

        # 程式碼 11-10
        # 接續在 request_body_json 變數之下
        # 產生 Headers
        headers = generate_linepay_headers(
            request_body=request_body_json,
            channel_id=channel_id,
            channel_secret=channel_secret,
            request_uri=api_path,
        )
        # 發送付款請求 Request API
        response = requests.post(
            url=request_api_url,
            headers=headers,
            data=request_body_json,
        )
        response_data = response.json()
        if response_data["returnCode"] == "0000":
            return Response(
                {"paymentUrl": response_data["info"]["paymentUrl"]},
                status=200,
            )
        return Response(
            {"detail": f"LINE Pay: {response_data['returnCode']}"},
            status=500,
        )

# 程式碼 11-18
class ConfirmView(APIView):
    def post(self, request):
        transaction_id = request.data.get("transactionId")
        order_id = request.data.get("orderId")

        if not re.fullmatch(r"\d{19}", transaction_id):
            return Response({"detail": "Invalid transaction_id"}, status=400)

        if not re.fullmatch(r"OD_\d{17}", order_id):
            return Response({"detail": "Invalid order_id"}, status=400)

        # 程式碼 11-19
        # 接續在 Invalid order_id 訊息之下
        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found"}, status=404)

        if order.line_pay_transaction_id != transaction_id:
            return Response({"detail": "Transaction mismatch"}, status=403)

        # 程式碼 11-20
        # 接續在 Transaction mismatch 訊息之下
        api_path = f"/v4/payments/{transaction_id}/confirm"
        confirm_api_url = f"{base_url}{api_path}"
        request_body = {
            "amount": order.total_amount,
            "currency": "TWD",
        }
        request_body_json = json.dumps(request_body)

        # 程式碼 11-21
        # 接續在 request_body_json 變數之下
        # 產生 Headers
        headers = generate_linepay_headers(
            request_body=request_body_json,
            channel_id=channel_id,
            channel_secret=channel_secret,
            request_uri=api_path,
        )
        # 發送付款請求 Confirm API
        response = requests.post(
            url=confirm_api_url,
            headers=headers,
            data=request_body_json,
        )
        # 程式碼 11-22
        # 接續在 response 變數之下
        response_data = response.json()
        if response_data["returnCode"] == "0000":
            # 更新訂單狀態為已付款
            order.payment_status = "paid"
            order.save()
            return Response({"detail": "Success"}, status=200)
        return Response(
            {"detail": f"LINE Pay Error: {response_data['returnCode']}"},
            status=400,
        )
