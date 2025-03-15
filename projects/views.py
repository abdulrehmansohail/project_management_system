from django.db import models
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Project, ProjectMember, Comment
from .serializers import ProjectSerializer, ProjectMemberSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

# Create your views here.

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            models.Q(owner=user) | models.Q(members__user=user)
        ).distinct()

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        ProjectMember.objects.create(
            project=project,
            user=self.request.user,
            role='OWNER'
        )
    
    def destroy(self, request, *args, **kwargs):
        project_obj = self.get_object()
        if self.request.user != project_obj.owner:
            raise PermissionDenied("You don't have permission to delete this project")
        self.perform_destroy(project_obj)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectMemberViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProjectMember.objects.filter(project__owner=self.request.user).exclude(role="OWNER")

    def create(self, request, *args, **kwargs):
        project_id = request.data.get('project')
        try:
            project = Project.objects.get(id=project_id, owner=request.user)
        except Project.DoesNotExist:
            raise PermissionDenied("You must be the project owner to add members")

        # Check if user is already a member
        if ProjectMember.objects.filter(project=project, user_id=request.data.get('user')).exists():
            raise serializers.ValidationError("User is already a member of this project")

        # Ensure role isn't OWNER
        if request.data.get('role') == 'OWNER':
            raise serializers.ValidationError("Cannot assign Owner role - project can only have one owner")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        member = self.get_object()
        if member.project.owner != request.user:
            raise PermissionDenied("Only project owner can remove members")
        return super().destroy(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.request.query_params.get("project_id")
        return Comment.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        project_id = serializer.validated_data.get("project").id
        # project_id = self.request.data._params.get("project_id")
        project = Project.objects.get(pk=project_id)
        try:
            member = ProjectMember.objects.get(project=project, user=self.request.user)
            if member.role not in ['OWNER', 'EDITOR']:
                raise PermissionDenied("Only Owners and Editors can comment on projects")
        except ProjectMember.DoesNotExist:
            raise PermissionDenied("You don't have access to this project")
        serializer.save(user=self.request.user, project=project)

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.user != self.request.user:
            raise PermissionDenied("You can only edit your own comments")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own comments")
        instance.delete()
