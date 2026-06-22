# 程式碼 6-7
from django.contrib import admin
from .models import Course
from import_export.admin import ImportExportModelAdmin

# 程式碼 7-25
from .models import CourseAlias

# 程式碼 6-7
@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    list_display = ('teacher_name','course_name')

# 程式碼 7-25
@admin.register(CourseAlias)
class CourseAliasAdmin(ImportExportModelAdmin):
    list_display = ('course_name', 'alias')
