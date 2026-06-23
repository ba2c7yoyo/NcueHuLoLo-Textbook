from django.db import models

# 程式碼 11-12
# Create your models here.
class Order(models.Model):
    order_id = models.CharField(max_length=20)
    line_pay_transaction_id = models.CharField(max_length=19)
    total_amount = models.PositiveIntegerField()
    payment_status = models.CharField(max_length=20, default="pending")
