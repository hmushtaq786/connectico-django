from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Organization, User, Workspace, Project, Team, InvitedUser, user_workspace_relation, Event, WorkspaceEvent, Post, WorkspacePost, WorkspacePostComment


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


class WorkspacePostDataSerializer(serializers.Serializer):
    pst_id = serializers.IntegerField()
    pst_content = serializers.CharField(max_length=200)
    created_on = serializers.DateTimeField()
    pst_filename = serializers.CharField(max_length=30)
    pst_filepath = serializers.CharField(max_length=255)
    created_by__id = serializers.IntegerField()
    created_by__first_name = serializers.CharField(max_length=200)
    created_by__last_name = serializers.CharField(max_length=200)
    created_by__photo_address = serializers.CharField(max_length=255)
    created_by__email = serializers.EmailField()


class WorkspacePostCommentDataSerializer(serializers.Serializer):
    c_id = serializers.IntegerField()
    c_content = serializers.CharField(max_length=200)
    created_on = serializers.DateTimeField()
    created_by__id = serializers.IntegerField()
    created_by__first_name = serializers.CharField(max_length=200)
    created_by__last_name = serializers.CharField(max_length=200)
    created_by__photo_address = serializers.CharField(max_length=255)


class WorkspacePostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspacePostComment
        fields = '__all__'
