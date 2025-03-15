from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from .views import ProjectViewSet, ProjectMemberViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'project-members', ProjectMemberViewSet, basename='project-member')
router.register(r'comments', CommentViewSet, basename='project-comments')

urlpatterns = [
    path('', include(router.urls)),
]
