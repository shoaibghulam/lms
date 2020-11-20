from django.contrib import admin
from .models import teacher,CourseCategory ,CourseLevel,Course,videos
# Dashboard Labeling
class TeacherAdmin(admin.ModelAdmin):
    list_display=('Name','uname','Occupation')

class CourseAdmin(admin.ModelAdmin):
    list_display=('Course_title','instructor_id','Course_category','Course_Level')

class CategoryAdmin(admin.ModelAdmin):
    list_display=('catid','cattitle')

class LavelAdmin(admin.ModelAdmin):
    list_display=('levelid','leveltitle')

class VideoAdmin(admin.ModelAdmin):
    list_display=('videoTitle','courseId')

admin.site.register(teacher,TeacherAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(CourseCategory,CategoryAdmin)
admin.site.register(CourseLevel,LavelAdmin)
admin.site.register(videos,VideoAdmin)

