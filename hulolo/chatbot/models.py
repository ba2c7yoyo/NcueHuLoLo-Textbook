# 程式碼 6-1
from django.db import models
from django.utils.translation import gettext_lazy as _
# 新增 Course類別
class Course(models.Model):
    # 程式碼 6-3
    class TypeInCourse(models.TextChoices):
        GENERAL = "GEN", _("通識課程")
        EDUCATION = "EDU", _("教育學程")
        PE_SOPHOMORE = "PSS", _("大二體育")
        PE_JUNIOR_SENIOR = "PJS", _("大三四體育")
        LANGUAGE = "LAN", _("精進中英外文")
        MILITARY = "MIL", _("軍訓")
    
    # 程式碼 6-2
    # 此行以下會有剛剛程式碼 6-2 的 Code
    course_type = models.CharField(
        max_length=3,
        verbose_name="類型",
    )

    # 程式碼 6-4
    # 此段程式碼位於 Course Class
    course_type = models.CharField(
        max_length=3,
        choices=TypeInCourse, # 選項引用自 TypeInCourse
        verbose_name="類型",
        default=TypeInCourse.GENERAL, # 預設為通識課程
    )
    # 程式碼 6-5
    course_name = models.CharField(
        max_length=20, 
        verbose_name="課名", 
        help_text="以教務系統顯示的全名為主"
    )

    teacher_name = models.CharField(
        max_length=20,
        verbose_name="老師/【合開】",
        help_text="【合開】連【】也要記得輸進去哦！",
    )

    submitter_name = models.CharField(
        max_length=15, 
        default="匿名", 
        verbose_name="投稿者", 
        help_text="不口以超過15字"
    )

    feedback_content = models.TextField(
        verbose_name="內容"
    )

    evaluation_semester = models.CharField(
        max_length=5,
        default="114-1",
    )

    last_updated_time = models.DateTimeField(
        auto_now=True, 
        verbose_name="上次修改日期"
)

# 程式碼 7-24
class CourseAlias(models.Model):
    course_name = models.CharField(max_length=20, 
                        verbose_name="全稱")
    alias = models.CharField(max_length=20, verbose_name="簡稱")

    def __str__(self):
        return self.alias

# 程式碼 9-10
class UserInfo(models.Model):
    user_id = models.CharField(
        unique=True, max_length=33, verbose_name="User ID")
    display_name = models.CharField(
        max_length=20, verbose_name="顯示名稱")
    year = models.CharField(
        max_length=4, verbose_name="系級")
    join_date = models.DateTimeField(
        auto_now=True, verbose_name="加入日期")

    def __str__(self):
        return self.display_name
