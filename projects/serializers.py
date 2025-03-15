from rest_framework import serializers
from .models import Project, ProjectMember, Comment

class ProjectSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'owner', 'owner_email']
        read_only_fields = ['owner', 'created_at', 'updated_at']

class ProjectMemberSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = ProjectMember
        fields = ['id', 'project', 'user', 'role', 'joined_at', 'user_email']
        read_only_fields = ['joined_at']

class CommentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'project', 'text', 'created_at', 'updated_at', 'user_email']
        read_only_fields = ['user', 'created_at', 'updated_at']
