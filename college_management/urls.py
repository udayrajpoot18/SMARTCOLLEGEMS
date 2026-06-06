from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.index, name='index'),
    path('login/', core_views.login_view, name='login'),
    path('logout/', core_views.logout_view, name='logout'),
    path('register/', core_views.register_view, name='register'),
    path('dashboard/', core_views.dashboard, name='dashboard'),
    path('profile/', core_views.profile_view, name='profile'),
    path('profile/update/', core_views.profile_update, name='profile_update'),
    path('settings/', core_views.settings_view, name='settings'),
    path('students/', include('apps.students.urls')),
    path('teachers/', include('apps.teachers.urls')),
    path('attendance/', include('apps.attendance.urls')),
    path('examinations/', include('apps.examinations.urls')),
    path('assignments/', include('apps.assignments.urls')),
    path('fees/', include('apps.fees.urls')),
    path('library/', include('apps.library.urls')),
    path('notices/', include('apps.notices.urls')),
    path('api/', include('apps.core.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
