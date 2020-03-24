from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Organization, User, Workspace, Project, Team, InvitedUser, user_workspace_relation


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
