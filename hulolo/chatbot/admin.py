# 程式碼 6-7
from django.contrib import admin
from .models import Course
from import_export.admin import ImportExportModelAdmin

# 程式碼 7-25
from .models import CourseAlias

# 程式碼 9-11
from .models import UserInfo

# 程式碼 6-7
@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    list_display = ('teacher_name','course_name')

# 程式碼 7-25
@admin.register(CourseAlias)
class CourseAliasAdmin(ImportExportModelAdmin):
    list_display = ('course_name', 'alias')

# 程式碼 9-11
@admin.register(UserInfo)
class UserInfoAdmin(ImportExportModelAdmin):
    list_display = ('display_name', 'year', 'join_date')
    search_fields = ('display_name', 'user_id', 'year')
