# 程式碼 10-4
# 此檔案於本地端不會被使用，專門為部署到 PythonAnywhere 而建立
# ......pythonanywhere_com_wsgi.py
import os
import dotenv
from django.core.wsgi import get_wsgi_application

# 特別留意路徑調整成你的 PythonAnywhere’s username
path = "/home/hulolo/hulolo/.env"
dotenv.read_dotenv(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hulolo.settings")

application = get_wsgi_application()