
from django.contrib import admin
from django.urls import path , include
#for images
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
  
    path('admin/', admin.site.urls),
    path('', include('lmsapp.urls')),
    path('teacher/', include('instructor.urls')),
    path('faculty/', include('faculty.urls')),
    path('student/', include('student.urls')),
    path('blog/', include('blog.urls')),
    path('event/', include('event.urls')),
    path('library/', include('library.urls')),
    path('videocalling/', include('administrator.urls')),
    path('chat/', include('chatapp.urls')),
    path('superadmin/', include('SuperAdmin.urls')),
    path('university/', include('UniversityApp.urls')),
    path('branch/', include('branch.urls')),



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'faculty.views.handler404'

