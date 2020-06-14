from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Organization, User, Workspace, Project, Team, Task, InvitedUser, user_workspace_relation, user_project_relation, user_team_relation, Event, WorkspaceEvent, ProjectEvent, TeamEvent, Post, WorkspacePost, ProjectPost, TeamPost, WorkspacePostComment, ProjectPostComment, TeamPostComment, Message


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


class TeamEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamEvent
        fields = '__all__'
        # fields = ('created_by_name',)


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        # fields = ('created_by_name',)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        # fields = ('created_by_name',)

# class TeamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Team
#         fields = '__all__'
#         # fields = ('created_by_name',)


class InvitedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitedUser
        fields = '__all__'
        # fields = ('created_by_name',)


class UserWorkspaceRelationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_workspace_relation
        fields = '__all__'


class UserProjectRelationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_project_relation
        fields = '__all__'


class UserTeamRelationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_team_relation
        fields = '__all__'


class MembersSerializer(serializers.Serializer):
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


class ProjectPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPost
        fields = '__all__'


class TeamPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamPost
        fields = '__all__'


class PostDataSerializer(serializers.Serializer):
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


class PostCommentDataSerializer(serializers.Serializer):
    c_id = serializers.IntegerField()
    c_content = serializers.CharField(max_length=200)
    created_on = serializers.DateTimeField()
    created_by__id = serializers.IntegerField()
    created_by__first_name = serializers.CharField(max_length=200)
    created_by__last_name = serializers.CharField(max_length=200)
    created_by__photo_address = serializers.CharField(max_length=255)


class UserWorkspaceDataSerializer(serializers.Serializer):
    uwr_id = serializers.IntegerField()
    u_id__id = serializers.IntegerField()
    w_id__w_id = serializers.IntegerField()
    w_id__w_name = serializers.CharField(max_length=30)
    w_id__description = serializers.CharField(max_length=200)
    w_id__w_address = serializers.CharField(max_length=200)
    w_id__created_on = serializers.DateTimeField()
    w_id__updated_on = serializers.DateTimeField()
    w_id__created_by__id = serializers.IntegerField()
    w_id__organization_id_id = serializers.IntegerField()


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


class UserTeamDataSerializer(serializers.Serializer):
    utr_id = serializers.IntegerField()
    u_id__id = serializers.IntegerField()
    t_id__tm_id = serializers.IntegerField()
    t_id__tm_name = serializers.CharField(max_length=30)
    t_id__tm_description = serializers.CharField(max_length=200)
    t_id__tm_start_date = serializers.DateField()
    t_id__tm_end_date = serializers.DateField()
    t_id__project_id__p_id = serializers.IntegerField()
    t_id__project_id__p_name = serializers.CharField(max_length=30)
    t_id__project_id__workspace_id__w_id = serializers.IntegerField()
    t_id__project_id__workspace_id__w_name = serializers.CharField(
        max_length=30)
    t_id__team_lead_id__id = serializers.IntegerField()
    t_id__created_on = serializers.DateTimeField()
    t_id__updated_on = serializers.DateTimeField()
    t_id__created_by__id = serializers.IntegerField()


class TeamUserDataSerializer(serializers.Serializer):
    utr_id = serializers.IntegerField()
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


class ProjectPostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPostComment
        fields = '__all__'


class TeamPostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamPostComment
        fields = '__all__'


class TestSerializer(serializers.Serializer):
    p_id = serializers.IntegerField()
    p_name = serializers.CharField(max_length=200)
    workspace_id__organization_id__id = serializers.IntegerField()
    workspace_id__w_id = serializers.IntegerField()


class AnotherTestSerializer(serializers.Serializer):
    tm_id = serializers.IntegerField()
    tm_name = serializers.CharField(max_length=200)
    project_id__workspace_id__organization_id__id = serializers.IntegerField()
    project_id__workspace_id__w_id = serializers.IntegerField()


class ConversationSerializer(serializers.Serializer):
    c_id = serializers.IntegerField()
    channel_name = serializers.CharField(max_length=20)
    sender__id = serializers.IntegerField()
    sender__username = serializers.CharField(max_length=50)
    sender__first_name = serializers.CharField(max_length=50)
    sender__last_name = serializers.CharField(max_length=50)
    sender__photo_address = serializers.CharField(max_length=200)
    receiver__id = serializers.IntegerField()
    receiver__username = serializers.CharField(max_length=50)
    receiver__first_name = serializers.CharField(max_length=50)
    receiver__last_name = serializers.CharField(max_length=50)
    receiver__photo_address = serializers.CharField(max_length=200)
    created_on = serializers.DateTimeField()


class MessageSerializer(serializers.Serializer):
    # class Meta:
    #     model = Message
    #     fields = '__all__'
    m_id = serializers.IntegerField()
    m_content = serializers.CharField(max_length=500)
    conversation__c_id = serializers.IntegerField()
    conversation__channel_name = serializers.CharField(max_length=20)
    sent_by__id = serializers.IntegerField()
    created_on = serializers.DateTimeField()
