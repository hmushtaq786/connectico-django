from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Organization, User, Workspace, Project, Team, InvitedUser, user_workspace_relation, Event, WorkspaceEvent, ProjectEvent, Post, WorkspacePost, WorkspacePostComment


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


class ProjectEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectEvent
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


class UserProjectDataSerializer(serializers.Serializer):
    upr_id = serializers.IntegerField()
    u_id__id = serializers.IntegerField()
    p_id__p_id = serializers.IntegerField()
    p_id__p_name = serializers.CharField(max_length=30)
    p_id__p_description = serializers.CharField(max_length=200)
    p_id__p_start_date = serializers.DateField()
    p_id__p_end_date = serializers.DateField()
    p_id__p_status = serializers.CharField(max_length=10)
    p_id__workspace_id__w_id = serializers.IntegerField()
    p_id__workspace_id__w_name = serializers.CharField(max_length=30)
    p_id__p_manager_id__id = serializers.IntegerField()
    p_id__created_on = serializers.DateTimeField()
    p_id__updated_on = serializers.DateTimeField()
    p_id__created_by__id = serializers.IntegerField()


class ProjectUserDataSerializer(serializers.Serializer):
    upr_id = serializers.IntegerField()
    u_id__id = serializers.IntegerField()
    u_id__username = serializers.CharField(max_length=200)
    u_id__first_name = serializers.CharField(max_length=200)
    u_id__last_name = serializers.CharField(max_length=200)
    u_id__email = serializers.EmailField()
    u_id__photo_address = serializers.CharField(max_length=200)
    u_id__organization_id = serializers.IntegerField()


class WorkspacePostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspacePostComment
        fields = '__all__'
