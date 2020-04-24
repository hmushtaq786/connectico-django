from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Organization, User, Workspace, Project, Team, InvitedUser, user_workspace_relation, Event, WorkspaceEvent, Post, WorkspacePost


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # model = User
        model = get_user_model()
        # fields = ('first_name', 'last_name')
        fields = '__all__'


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        # model = User
        model = get_user_model()
        # fields = ('first_name', 'last_name')
        fields = ('id', 'first_name', 'last_name', 'email', 'photo_address')


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        # fields = ('created_by_name',)


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = '__all__'
        # fields = ('created_by_name',)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        # fields = ('created_by_name',)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        # fields = ('created_by_name',)


class WorkspaceEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceEvent
        fields = '__all__'
        # fields = ('created_by_name',)


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        # fields = ('created_by_name',)


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        # fields = ('created_by_name',)


class InvitedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitedUser
        fields = '__all__'
        # fields = ('created_by_name',)


class UserWorkspaceRelationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_workspace_relation
        fields = '__all__'


class WorkspaceMembersSerializer(serializers.Serializer):
    u_id__id = serializers.IntegerField()
    u_id__first_name = serializers.CharField(max_length=200)
    u_id__last_name = serializers.CharField(max_length=200)
    u_id__photo_address = serializers.CharField(max_length=255)
    u_id__email = serializers.EmailField()


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class WorkspacePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspacePost
        fields = '__all__'
