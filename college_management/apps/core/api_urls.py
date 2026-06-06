from django.urls import path
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register('users', api_views.UserViewSet)
router.register('departments', api_views.DepartmentViewSet)
router.register('courses', api_views.CourseViewSet)

urlpatterns = router.urls
