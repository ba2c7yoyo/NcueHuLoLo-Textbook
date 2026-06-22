from django.shortcuts import render
# Create your views here.
# 程式碼 5-4
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponse
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, ImageSendMessage
from linebot.exceptions import InvalidSignatureError, LineBotApiError

# 程式碼 7-1 新增引入 models 及 TextSendMessage
from .models import *
from linebot.models import TextSendMessage
# 程式碼 7-7 新增引入 FlexSendMessage
from linebot.models import FlexSendMessage
from pathlib import Path
import os

# 程式碼 7-12 新增引入 PostbackEvent
from linebot.models import PostbackEvent

# 程式碼 7-7
# 宣告一個路徑代表此資料夾的位置稍後要引入 JSON
BASE_DIR = Path(__file__).resolve().parent.parent

# 程式碼 5-4
parser = WebhookHandler(settings.LINE_CHANNEL_SECRET)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
@csrf_exempt # 關閉CSRF
def callback(request):
    # 確認請求是來自 LINE 的 webhook
    signature = request.META['HTTP_X_LINE_SIGNATURE']

    # 取得 request body
    body = request.body.decode('utf-8')
   
    try:
    # 驗證來自 LINE 的簽名
        parser.handle(body, signature)
    except InvalidSignatureError:
        return HttpResponseForbidden()
    except LineBotApiError:
        return HttpResponseForbidden()

    return HttpResponse('OK')

# 程式碼 5-5
def reply_cat_url():
    url = "https://api.thecatapi.com/v1/images/search?limit=1"
    response = requests.get(url)
    content = json.loads(response.text) # 回應的文字以JSON格式解開
    image_url = content[0]["url"]
    return image_url

# 程式碼 5-6 (此函式已於 Ch07 章節被修改)
# 程式碼 7-1
# 程式碼 7-6
# 處理訊息的事件
@parser.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text  # 取得使用者發送的文字

    # 程式碼 7-2
    # 接續上一步程式碼
    if "-" in user_message:
        teacher_name = user_message.split("-")[0]
        course_name = user_message.split("-")[1]

        # 程式碼 7-3
        # 接續上一步程式碼
        filtered_courses = Course.objects.filter(
                                    teacher_name =
                                    teacher_name, 
                                    course_name = course_name
                                    )[:5]

        # 程式碼 7-4
        # 接續上一步程式碼
        if filtered_courses.exists():
            messages = []

            # ---程式碼 7-4 開始(以下程式碼將於程式碼 7-9 被修改)---
            # for course in filtered_courses:
            #     messages.append(TextSendMessage(
            #     text=f"""課程: {course.course_name}\n評價: {course.feedback_content}
            #     """))
            # ---程式碼 7-4 結束(以上程式碼將於程式碼 7-9 被修改)---

            # ---程式碼 7-10 開始(以下程式碼將於程式碼 7-10 才出現)---
            # 在原本位置加入程式碼
            for idx, course in enumerate(filtered_courses, start=1):  
                # 準備課程資料以傳入 flex_message_package 函式
                course_info = {
                    'course_name': course.course_name,
                    'teacher_name': course.teacher_name,
                    'course_type': course.course_type,
                    'feedback_content': course.feedback_content,
                    'evaluation_semester': course.evaluation_semester,
                    'submitter_name': course.submitter_name,
                    'number': str(idx),  # 這裡的 idx 是第幾則的意思
                    }
                # 呼叫 flex_message_package 函式來產生 Flex Message
                flex_message = flex_message_package(course_info)    

                # 以 `FlexSendMessage` 類型打包訊息
                messages.append(FlexSendMessage(
                                alt_text=f"課程評價：{course.course_name}",
                                contents=flex_message
                            ))
            # 以下程式碼不變動，注意它沒有被包在迴圈哦!
            line_bot_api.reply_message
            # ---程式碼 7-10 結束(以上程式碼將於程式碼 7-10 才出現)---

            # 程式碼 7-5
            # 接續上一步程式碼
            line_bot_api.reply_message(
                event.reply_token,
                messages  # 回覆所有 messages 陣列中的值
            )
        # 程式碼 7-6 新增的部分 (留意縮排)
        else:
            print("Empty")

# 程式碼 7-8
def flex_message_package(course_info):
    # JSON 評價回覆格式檔案路徑
    json_path = os.path.join(BASE_DIR, 'chatbot', 'reply_evaluation.json')
    # Python 是看不懂 JSON 的，需要轉為字典形式
    flex = json.load(open(json_path, 'r', encoding='utf-8'))

    # 這裡是 JSON 中每個會成為變數的位置，將其換成真正資料表中的變數
    flex['header']['contents'][0]['text'] = course_info['course_name']
    flex['header']['contents'][1]['text'] = course_info['teacher_name']
    flex['body']['contents'][0]['contents'][0]['contents'][0]['text'] = course_info['feedback_content']
    flex['body']['contents'][0]['contents'][2]['contents'][1]['text'] = course_info['course_type']
    flex['body']['contents'][0]['contents'][3]['contents'][1]['text'] = course_info['evaluation_semester']
    flex['body']['contents'][0]['contents'][4]['contents'][1]['text'] = course_info['submitter_name']
    flex['footer']['contents'][0]['contents'][0]['text'] = f"{course_info['teacher_name']}-{course_info['course_name']}"
    flex['footer']['contents'][0]['contents'][1]['text'] = f"第{course_info['number']}則"

    return flex

# 程式碼 7-14
def teacher_lists_flex_message_package(teacher_name, candidate_courses):
    # 引入 JSON 檔案
    json_path = os.path.join(BASE_DIR, 
        'chatbot', 'reply_course_list.json')
    flex = json.load(open(json_path, 'r', encoding='utf-8'))    

    # 設定標題為老師名稱
    flex['body']['contents'][0]['text'] = f"{teacher_name}老師的哪堂課?"

    # 課程列表的選項用了十個顏色!
    colors = ['#F0C29E', '#A1DE95', '#F5C578', '#91D9C2', '#DFC493', 
            '#F0C29E', '#A1DE95', '#F5C578', '#91D9C2', '#DFC493']

    # 根據上述顏色動態生成課程按鈕，而且是根據幾堂課就產生幾個按鈕~
    
    # 程式碼 7-15
    # 接續上段程式碼
    for i, course in enumerate(candidate_courses, start=1):
        button = {
            'type': 'box',
            'layout': 'vertical',
            'spacing': 'none',
            'contents': [{
                'type': 'button',
                'style': 'primary',
                'action': {
                    'type': 'postback',
                    'label': course,
                    #注意! 這很重要，此處代表按鈕背後真正的資料
                    'data': f"{teacher_name}-{course}" 
                },
                'color': colors[i-1],
                'margin': 'xs',
                'offsetTop': 'none',
                'height': 'sm'
            }],
            'flex': 0,
            'borderWidth': 'medium',
            'cornerRadius': 'xxl',
            'offsetTop': 'none',
            'margin': 'md',
            'backgroundColor': colors[i-1]
        }
        flex['body']['contents'].append(button)
    return flex

# 程式碼 7-13
@parser.add(MessageEvent, message=TextMessage)
def handle_teacher_name_msg(event):    
    user_message = event.message.text  # 取得使用者發送的文字
    filtered_teacher = Course.objects.filter(teacher_name=user_message)
    if filtered_teacher.exists(): 
        teacher_name = user_message

        # values_list 是以陣列裝課程名稱
        # distinct 可以把可能重複的老師名做過濾
        candidate_courses = filtered_teacher.values_list(
        'course_name', flat=True).distinct()

        # 稍後會製作這個漂亮的函式，先呼叫它
        flex_message = teacher_lists_flex_message_package(
        teacher_name, candidate_courses)

        message = FlexSendMessage(
                            alt_text=f"{teacher_name} 老師的課程",
                            contents=flex_message
                        )
        line_bot_api.reply_message(
                    event.reply_token,
                    message)
    else:
        print("Empty")

# 程式碼 7-16
@parser.add(PostbackEvent)
def handle_postback(event): 
    # 取得使用者點按鈕時回傳的資料
    postback_data = event.postback.data

    # 還記得前面提及按鈕背後的資料嗎? 在這!
    # postback_data 格式為 "課程名稱-老師名稱"
    if "-" in postback_data:
        teacher_name = postback_data.split("-")[0]
        course_name = postback_data.split("-")[1]

        filtered_courses = Course.objects.filter(
            teacher_name=teacher_name, course_name=course_name)[:5]
        if filtered_courses.exists():
            messages = []
            
        # 程式碼 7-17
        # 使用 enumerate 給每個課程加上編號，下一行與messages縮排對齊
            for idx, course in enumerate(filtered_courses, start=1):  

                # 準備課程資料以傳入 flex_message_package 函式
                course_info = {
                    'course_name': course.course_name,
                    'teacher_name': course.teacher_name,
                    'course_type': course.course_type,
                    'feedback_content': course.feedback_content,
                    'evaluation_semester': course.evaluation_semester,
                    'submitter_name': course.submitter_name,
                    'number': str(idx),  # 這裡的 idx 是第幾則的意思
                    }
        # 程式碼 7-18
        # 呼叫 flex_message_package 函式產生 Flex Messag，下一行與course_info縮排對齊
                flex_message = flex_message_package(course_info)

                # 使用 FlexSendMessage 回傳 Flex Message
                messages.append(FlexSendMessage(
                        alt_text=f"課程評價：{course.course_name}",
                        contents=flex_message
                    ))

                line_bot_api.reply_message(
                    event.reply_token,
                    messages  # 回傳 Flex Message 列表
                )         
            else:
                print("Empty")
        else:
            print("Empty")

# 程式碼 7-22
def dynamic_flex_message_package(title_name, 
    candidate_list, label_type):
    # 引入 JSON 檔案
    json_path = os.path.join(BASE_DIR, 'chatbot', 
                 'reply_course_teacher_list.json')
    flex = json.load(open(json_path, 'r', encoding='utf-8'))    

    # 設定標題為傳入的名稱 (可以是老師名或課程名) 這邊使用了單行條件句
    flex['body']['contents'][0]['text'] = f"哪位老師的{title_name}?" if label_type == 'teacher' else f"{title_name}老師的哪堂課?"

    # 設定顏色列表
    colors = ['#F0C29E', '#A1DE95', '#F5C578', '#91D9C2', '#DFC493', 
              '#F0C29E', '#A1DE95', '#F5C578', '#91D9C2', '#DFC493']

    # 程式碼 7-23
    # 接續上方程式碼
    # 根據傳入的 candidate_list 動態生成按鈕
    for i, name in enumerate(candidate_list, start=1):
        button = {
            'type': 'box',
            'layout': 'vertical',
            'spacing': 'none',
            'contents': [{
                'type': 'button',
                'style': 'primary',
                'action': {
                    'type': 'postback',
                    'label': name,

        # 注意這裡的 data 格式，使用了條件句，根據傳入的參數動態生成資料
        # 因為兩者課名與老師名的順序對調會讓 handle_postback 失效 
                    'data': f"{name}-{title_name}" if 
                        label_type == "teacher" else f"{title_name}-{name}" 
                },
                'color': colors[i-1],
                'margin': 'xs',
                'offsetTop': 'none',
                'height': 'sm'
            }],
            'flex': 0,
            'borderWidth': 'medium',
            'cornerRadius': 'xxl',
            'offsetTop': 'none',
            'margin': 'md',
            'backgroundColor': colors[i-1]
        }
        flex['body']['contents'].append(button)
    return flex

# 程式碼 7-19
@parser.add(MessageEvent, message=TextMessage)
def handle_msg(event):    
    user_message = event.message.text  # 取得使用者發送的文字
  
    # 以不同條件做搜尋
    filtered_teacher = Course.objects.filter(teacher_name=user_message)
    filtered_course = Course.objects.filter(course_name=user_message)
    
    # 程式碼 7-26
    # 新增了對課名簡稱資料表的搜尋
    filtered_course_alias = CourseAlias.objects.filter(alias=user_message)

    # 程式碼 7-20
    # 接續上段程式碼
    # 判斷老師名的物件是否存在資料
    if filtered_teacher.exists():
        teacher_name = user_message
        # values_list 是以陣列裝課程名稱
        # distinct 可以把可能重複的老師名做過濾
        candidate_courses = filtered_teacher.values_list(
            'course_name', flat=True).distinct()
        # 稍後會製作這個漂亮的函式，先呼叫它
        flex_message = dynamic_flex_message_package(
            teacher_name, candidate_courses, label_type='course')

        message = FlexSendMessage(
            alt_text=f"{teacher_name} 老師的課程", 
            contents=flex_message)
        line_bot_api.reply_message(event.reply_token, message)

    # 程式碼 7-21
    # 接續上段程式碼
    # 判斷課程名的物件是否存在資料
    elif filtered_course.exists():
        course_name = user_message
        candidate_teachers = filtered_course.values_list(
        'teacher_name', flat=True).distinct()

        # 同樣地，稍後會製作這個漂亮的函式，先呼叫它
        # 多了 label_type 變數讓函式能辨識
        flex_message = dynamic_flex_message_package(
        course_name, candidate_teachers, label_type='teacher')

        message = FlexSendMessage(
                            alt_text=f"{course_name} 的老師",
                            contents=flex_message
                        )
        line_bot_api.reply_message(event.reply_token, message)

    # 程式碼 7-27
    # 如果課名簡稱資料表有值
    elif filtered_course_alias.exists():
        # 取得所有對應的課程名稱，這裡假設簡稱不會重複對應到多個課程
        full_course_name = filtered_course_alias.values_list('course_name', flat=True).first()

        # 根據課程名稱查詢對應的老師
        filtered_course = Course.objects.filter(course_name=full_course_name).values_list(
            'teacher_name', flat=True).distinct()

        # 將查詢結果轉換為候選老師列表
        candidate_teachers = list(filtered_course)

        # 呼叫動態生成訊息的函式，顯示老師的選擇
        flex_message = dynamic_flex_message_package(
            full_course_name, candidate_teachers, label_type='teacher')

        message = FlexSendMessage(
            alt_text=f"{full_course_name} 的老師",
            contents=flex_message
        )

        # 回覆訊息給使用者
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    else:
        print("Empty")
