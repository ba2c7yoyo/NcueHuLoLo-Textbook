"""
URL configuration for hulolo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# 程式碼 5-3
from chatbot.views import *
urlpatterns = [
    path("admin/", admin.site.urls),
    # 新增 callback 函式
    path('chatbot', callback),

    # 程式碼 8-1，記得上兩行的 callback 括號後要加上逗號
    # 空白 '' 代表其根網址就是評價瀏覽頁面
    path('', course_feedback),
]
