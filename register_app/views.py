import pusher
from django.core.mail import send_mail
from password_generator import PasswordGenerator
import re
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from django.contrib.auth.hashers import make_password
from django.db import connection
from django.db.models import Q
###MODELS###
from .models import Organization, Workspace, Project, Team, Task, InvitedUser, user_workspace_relation, Event, WorkspaceEvent, ProjectEvent, TeamEvent, Post, WorkspacePost, ProjectPost, TeamPost, WorkspacePostComment, ProjectPostComment, TeamPostComment, user_project_relation, user_team_relation, Message

###SERIALIZERS###
from .serializers import UserSerializer, OrganizationSerializer, UserMiniSerializer, WorkspaceSerializer, ProjectSerializer, TeamSerializer, InvitedUserSerializer, UserWorkspaceRelationsSerializer, UserProjectRelationsSerializer, EventSerializer, WorkspaceEventSerializer, ProjectEventSerializer, TeamEventSerializer, MembersSerializer, PostSerializer, WorkspacePostSerializer, ProjectPostSerializer, TeamPostSerializer, PostDataSerializer, WorkspacePostCommentSerializer, ProjectPostCommentSerializer, TeamPostCommentSerializer, PostCommentDataSerializer, UserProjectDataSerializer, ProjectUserDataSerializer, UserTeamDataSerializer, TeamUserDataSerializer, UserTeamRelationsSerializer, TaskSerializer, TestSerializer, AnotherTestSerializer, UserWorkspaceDataSerializer, MessageSerializer

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    authentication_classes = (BasicAuthentication,)

    def create(self, request):
        # queryset = get_user_model().objects.all()
        # serializer = UserSerializer(queryset, many=True)

        # print(request.data)
        # if request.data['status_line']:
        #     request.data['status_line'] = ''
        #     print(hi1)
        # if request.data['phone_number']:
        #     request.data['phone_number'] = ''
        #     print(hi2)
        # if request.data['photo_address']:
        #     request.data['photo_address'] = ''
        #     print(hi3)

        if request.method == 'POST':
            _mutable = request.data._mutable
            request.data._mutable = True
            if request.data.get('organization_id'):
                org_id = request.data['organization_id']
                queryset = Organization.objects.filter(id=org_id)
                org = get_object_or_404(queryset,)
            else:
                org = None
            user = get_user_model().objects.create(
                email=request.data['email'],
                username=request.data['username'],
                password=make_password(request.data['password']),
                first_name=request.data['first_name'],
                last_name=request.data['last_name'],
                status_line=request.data.setdefault('status_line', ''),
                phone_number=request.data.setdefault('phone_number', ''),
                photo_address=request.data.setdefault('photo_address', ''),
                organization_id=org)

            serializer = UserSerializer(user)
            request.data._mutable = _mutable
        else:
            queryset = get_user_model().objects.all()
            serializer = UserSerializer(queryset, many=True)

        return Response(serializer.data)

    # @list_route(methods=['get'], url_path='users/(?P<username>\w+)')
    # def getByUsername(self, request, username):
    #     user = get_object_or_404(User, username=username)
    #     return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        # lookup_value_regex = '[\w.]+'
        if(pk.isdigit()):
            queryset = get_user_model().objects.filter(id=pk)
            user = get_object_or_404(queryset,)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            queryset = get_user_model().objects.filter(username=pk)
            user = get_object_or_404(queryset,)
            serializer = UserSerializer(user)
            return Response(serializer.data)

    # def update(self, request, pk=None):
    #     queryset = get_user_model().objects.filter(id=pk)
    #     user = get_object_or_404(queryset,)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)

    # def list(self, request):
    #     if(request.method == 'GET'):
    #         print('lol', request.data)
    #         queryset = get_user_model().objects.all()
    #         serializer = UserSerializer(queryset, many=True)
    #         authentication_classes = (TokenAuthentication,)
    #         return Response(serializer.data)

    #     if(request.method == 'POST'):
    #         print(request.POST)

    # def list(self, request):
    #     print('list')
    #     queryset = get_user_model().objects.all()
    #     serializer = UserSerializer(queryset, many=True)
    #     authentication_classes = (TokenAuthentication,)
    #     return Response(serializer.data)
    # def create(self, request):
    #     print('create')
    #     queryset = get_user_model().objects.all()
    #     serializer = UserSerializer(queryset, many=True)
    #     authentication_classes = []
    #     return Response(serializer.data)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    authentication_classes = (TokenAuthentication,)

    # def retrieve(self, request, pk=None):
    # lookup_value_regex = '[\w.]+'

    # if pk[0:1] is 'l':

    # print(pk[0:1])
    # queryset = Organization.objects.filter(created_by=pk)
    # organization = get_object_or_404(queryset,)
    # serializer = OrganizationSerializer(organization)
    # return Response(serializer.data)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        action = pk[0]
        pk = pk[1:]
        if action == 'w':  # to search using the workspace_id
            queryset = Project.objects.filter(workspace_id=pk)

        elif action == 'p':  # to search using the project_id
            queryset = Project.objects.filter(p_id=pk)

        projects = get_list_or_404(queryset,)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class UserWorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        action = pk[0]
        pk = pk[1:]

        serializer = {'data': ''}

        if action == 'u':  # to search using the user_id
            queryset = user_workspace_relation.objects.select_related(
                'u_id', 'w_id').values(
                'uwr_id', 'u_id__id', 'w_id__w_id', 'w_id__w_name', 'w_id__description', 'w_id__w_address', 'w_id__created_on', 'w_id__updated_on', 'w_id__created_by__id', 'w_id__organization_id_id').filter(u_id=pk).order_by('w_id')
            projects = get_list_or_404(queryset,)
            serializer = UserWorkspaceDataSerializer(projects, many=True)

        elif action == 'p':  # to search using the project_id
            queryset = user_project_relation.objects.select_related(
                'u_id', 'p_id').values(
                'upr_id', 'u_id__id', 'u_id__username', 'u_id__first_name', 'u_id__last_name', 'u_id__email', 'u_id__photo_address', 'u_id__organization_id').filter(p_id=pk)
            projects = get_list_or_404(queryset,)
            serializer = ProjectUserDataSerializer(projects, many=True)

        elif action == 'o':  # to search using the org_id
            queryset = Project.objects.select_related(
                'workspace_id').values(
                'p_id', 'p_name', 'workspace_id__w_id', 'workspace_id__organization_id__id').filter(workspace_id__organization_id__id=pk)
            projects = get_list_or_404(queryset,)
            serializer = TestSerializer(projects, many=True)

        return Response(serializer.data)


class UserProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        action = pk[0]
        pk = pk[1:]

        serializer = {'data': ''}

        if action == 'u':  # to search using the user_id
            queryset = user_project_relation.objects.select_related(
                'u_id', 'p_id').values(
                'upr_id', 'u_id__id', 'p_id__p_id', 'p_id__p_name', 'p_id__p_description', 'p_id__p_start_date', 'p_id__p_end_date', 'p_id__p_status', 'p_id__workspace_id__w_id', 'p_id__workspace_id__w_name', 'p_id__p_manager_id__id', 'p_id__created_on', 'p_id__updated_on', 'p_id__created_by__id').filter(u_id=pk).order_by('p_id')
            projects = get_list_or_404(queryset,)
            serializer = UserProjectDataSerializer(projects, many=True)

        elif action == 'p':  # to search using the project_id
            queryset = user_project_relation.objects.select_related(
                'u_id', 'p_id').values(
                'upr_id', 'u_id__id', 'u_id__username', 'u_id__first_name', 'u_id__last_name', 'u_id__email', 'u_id__photo_address', 'u_id__organization_id').filter(p_id=pk)
            projects = get_list_or_404(queryset,)
            serializer = ProjectUserDataSerializer(projects, many=True)

        elif action == 'o':  # to search using the org_id
            queryset = Project.objects.select_related(
                'workspace_id').values(
                'p_id', 'p_name', 'workspace_id__w_id', 'workspace_id__organization_id__id').filter(workspace_id__organization_id__id=pk)
            projects = get_list_or_404(queryset,)
            serializer = TestSerializer(projects, many=True)

        return Response(serializer.data)


class UserTeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        action = pk[0]
        pk = pk[1:]

        serializer = {'data': ''}

        if action == 'u':  # to search using the user_id
            queryset = user_team_relation.objects.select_related(
                'u_id', 't_id').values(
                'utr_id', 'u_id__id', 't_id__tm_id', 't_id__tm_name', 't_id__tm_description', 't_id__tm_start_date', 't_id__tm_end_date', 't_id__project_id__p_id', 't_id__project_id__p_name', 't_id__project_id__workspace_id__w_id', 't_id__project_id__workspace_id__w_name', 't_id__team_lead_id__id', 't_id__created_on', 't_id__updated_on', 't_id__created_by__id').filter(u_id=pk).order_by('t_id')
            teams = get_list_or_404(queryset,)
            serializer = UserTeamDataSerializer(teams, many=True)

        elif action == 't':  # to search using the team_id
            queryset = user_team_relation.objects.select_related(
                'u_id', 't_id').values(
                'utr_id', 'u_id__id', 'u_id__username', 'u_id__first_name', 'u_id__last_name', 'u_id__email', 'u_id__photo_address', 'u_id__organization_id').filter(t_id=pk)
            teams = get_list_or_404(queryset,)
            serializer = TeamUserDataSerializer(teams, many=True)

        elif action == 'o':  # to search using the org_id
            queryset = Team.objects.select_related(
                'project_id').values(
                'tm_id', 'tm_name', 'project_id__workspace_id__w_id', 'project_id__workspace_id__organization_id__id').filter(project_id__workspace_id__organization_id__id=pk)
            projects = get_list_or_404(queryset,)
            serializer = AnotherTestSerializer(projects, many=True)

        return Response(serializer.data)


class OrganizationUsersViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserMiniSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        queryset = get_user_model().objects.filter(organization_id=pk)
        users = get_list_or_404(queryset,)
        serializer = UserMiniSerializer(users, many=True)
        return Response(serializer.data)


class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        queryset = Workspace.objects.filter(organization_id=pk)
        workspaces = get_list_or_404(queryset,)
        serializer = WorkspaceSerializer(workspaces, many=True)
        return Response(serializer.data)


class WorkspaceMembersViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = MembersSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):

        queryset = user_workspace_relation.objects.select_related(
            'w_id', 'u_id').values('u_id__id', 'u_id__first_name', 'u_id__last_name', 'u_id__photo_address', 'u_id__email').filter(w_id=pk)

        # print(queryset.query)

        serializer = MembersSerializer(queryset, many=True)
        return Response(serializer.data)


class ProjectMembersViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = MembersSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        queryset = user_project_relation.objects.select_related(
            'p_id', 'u_id').values('u_id__id', 'u_id__first_name', 'u_id__last_name', 'u_id__photo_address', 'u_id__email').filter(p_id=pk)

        serializer = MembersSerializer(queryset, many=True)
        return Response(serializer.data)


class OrganizationProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.select_related('workspace_id', '')
    serializer_class = ProjectSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        queryset = Project.objects.filter(organization_id=pk)
        workspaces = get_list_or_404(queryset,)
        serializer = WorkspaceSerializer(workspaces, many=True)
        return Response(serializer.data)


class OrganizationInvitedUserViewSet(viewsets.ModelViewSet):
    queryset = InvitedUser.objects.all()
    serializer_class = InvitedUserSerializer
    authentication_classes = (TokenAuthentication,)

    # def retrieve(self, request, pk=None):
    #     queryset = InvitedUser.objects.filter(organization_id=pk)
    #     print(queryset)
    #     invited_users = get_list_or_404(queryset,)
    #     serializer = InvitedUserSerializer(invited_users, many=True)
    #     print(serializer)
    #     print(serializer.data)
    #     return Response(serializer.data)


class FirstTimeUserAuth(APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request):

        return Response(request.method)

    def post(self, request):
        queryset = InvitedUser.objects.filter(
            email=request.data['email'], password=request.data['password'])
        new_user = get_object_or_404(queryset,)
        serializer = InvitedUserSerializer(new_user, many=False)
        return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     queryset = InvitedUser.objects.filter(organization_id=pk)
    #     print(queryset)
    #     invited_users = get_list_or_404(queryset,)
    #     serializer = InvitedUserSerializer(invited_users, many=True)
    #     print(serializer)
    #     print(serializer.data)
    #     return Response(serializer.data)


class InviteMembers(APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request):

        return Response(request.method)

    def post(self, request):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        valid_emails = []
        pwo = PasswordGenerator()
        pwo.minlen = 20
        pwo.maxlen = 20
        pwo.minuchars = 3
        pwo.minlchars = 3
        pwo.minnumbers = 5
        pwo.minschars = 3
        pwo.excludeschars = ".,;:"

        for email in request.data['list']:
            if(re.search(regex, email)):
                queryset = Organization.objects.filter(
                    id=request.data['org_id'])
                org = get_object_or_404(queryset,)
                password = pwo.generate()
                store_invited_email = InvitedUser.objects.create(
                    email=email, password=password, organization_id=org)
                send_mail(
                    'Login Credentials',
                    f'''
                Good day!
                You've been invited to join {org} at Connectico. Please use the given credentials to login at 127.0.0.1:4200.
                
                Email: {email}
                Password: {password}

                Regards,
                Connectico Team
                ''',
                    'Connectico Team',
                    [email],
                    fail_silently=False,
                )
                valid_emails.append(email)
            else:
                print('Discarded', email)

        return Response(valid_emails)


class UserWorkspaceRelationViewSet(viewsets.ModelViewSet):
    queryset = user_workspace_relation.objects.all()
    serializer_class = UserWorkspaceRelationsSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        action = pk[0]
        pk = pk[1:]
        if action == 'u':  # to search using the user_id
            queryset = user_workspace_relation.objects.filter(u_id=pk)

        elif action == 'w':  # to search using the workspace_id
            queryset = user_workspace_relation.objects.filter(w_id=pk)

        data = get_list_or_404(queryset,)
        serializer = UserWorkspaceRelationsSerializer(data, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        splited_key = pk.split('w')
        user_id = splited_key[0]
        user_id = int(user_id[1:])
        workspace_id = int(splited_key[1])

        queryset = user_workspace_relation.objects.filter(
            u_id=user_id, w_id=workspace_id)
        queryset.delete()
        return Response(queryset)


class UserProjectRelationViewSet(viewsets.ModelViewSet):
    queryset = user_project_relation.objects.all()
    serializer_class = UserProjectRelationsSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        action = pk[0]
        pk = pk[1:]
        if action == 'u':  # to search using the user_id
            queryset = user_project_relation.objects.filter(u_id=pk)

        elif action == 'p':  # to search using the project_id
            queryset = user_project_relation.objects.filter(p_id=pk)

        data = get_list_or_404(queryset,)
        serializer = UserProjectRelationsSerializer(data, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        splited_key = pk.split('p')
        user_id = splited_key[0]
        user_id = int(user_id[1:])
        project_id = int(splited_key[1])

        queryset = user_project_relation.objects.filter(
            u_id=user_id, p_id=project_id)
        queryset.delete()
        return Response(queryset)


class UserTeamRelationViewSet(viewsets.ModelViewSet):
    queryset = user_team_relation.objects.all()
    serializer_class = UserTeamRelationsSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        action = pk[0]
        pk = pk[1:]
        if action == 'u':  # to search using the user_id
            queryset = user_team_relation.objects.filter(u_id=pk)

        elif action == 't':  # to search using the team_id
            queryset = user_team_relation.objects.filter(t_id=pk)

        data = get_list_or_404(queryset,)
        serializer = UserTeamRelationsSerializer(data, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        splited_key = pk.split('t')
        user_id = splited_key[0]
        user_id = int(user_id[1:])
        team_id = int(splited_key[1])

        queryset = user_team_relation.objects.filter(
            u_id=user_id, t_id=team_id)
        queryset.delete()
        return Response(queryset)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = (TokenAuthentication,)


class WorkspaceEventViewSet(viewsets.ModelViewSet):
    queryset = WorkspaceEvent.objects.all()
    serializer_class = WorkspaceEventSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        action = pk[0]
        pk = pk[1:]
        if action == 'w':  # to search using the workspace_id
            queryset = WorkspaceEvent.objects.filter(workspace_id=pk)

        elif action == 'e':  # to search using the event_id
            queryset = WorkspaceEvent.objects.filter(e_id=pk)

        events = get_list_or_404(queryset,)
        serializer = WorkspaceEventSerializer(events, many=True)
        return Response(serializer.data)


class ProjectEventViewSet(viewsets.ModelViewSet):
    queryset = ProjectEvent.objects.all()
    serializer_class = ProjectEventSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        action = pk[0]
        pk = pk[1:]
        if action == 'p':  # to search using the project_id
            queryset = ProjectEvent.objects.filter(project_id=pk)

        elif action == 'e':  # to search using the event_id
            queryset = ProjectEvent.objects.filter(e_id=pk)

        events = get_list_or_404(queryset,)
        serializer = ProjectEventSerializer(events, many=True)
        return Response(serializer.data)


class TeamEventViewSet(viewsets.ModelViewSet):
    queryset = TeamEvent.objects.all()
    serializer_class = TeamEventSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        action = pk[0]
        pk = pk[1:]
        if action == 't':  # to search using the team_id
            queryset = TeamEvent.objects.filter(team_id=pk)

        elif action == 'e':  # to search using the event_id
            queryset = TeamEvent.objects.filter(e_id=pk)

        events = get_list_or_404(queryset,)
        serializer = TeamEventSerializer(events, many=True)
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)


class WorkspacePostViewSet(viewsets.ModelViewSet):
    queryset = WorkspacePost.objects.all()
    serializer_class = WorkspacePostSerializer
    authentication_classes = (TokenAuthentication,)

# def retrieve(self, request, pk=None):

#         queryset = user_workspace_relation.objects.select_related(
#             'w_id', 'u_id').values('u_id__id', 'u_id__first_name', 'u_id__last_name', 'u_id__photo_address', 'u_id__email').filter(w_id=pk)

#         # print(queryset.query)

#         serializer = MembersSerializer(queryset, many=True)
#         return Response(serializer.data)

    def retrieve(self, request, pk=None):
        action = pk[0]
        pk = pk[1:]
        if action == 'w':  # to search using the workspace_id
            # queryset = WorkspacePost.objects.filter(workspace_id=pk)
            # queryset = user_workspace_relation.objects.select_related(
            # 'w_id', 'u_id').values('u_id__id', 'u_id__first_name', 'u_id__last_name', 'u_id__photo_address', 'u_id__email').filter(w_id=pk)

            queryset = WorkspacePost.objects.select_related('created_by').values(
                'pst_id', 'pst_content', 'created_on', 'pst_filename', 'pst_filepath', 'created_by__id', 'created_by__first_name', 'created_by__last_name', 'created_by__photo_address', 'created_by__email').filter(workspace_id=pk).order_by('-created_on')

        elif action == 'p':  # to search using the post_id
            queryset = WorkspacePost.objects.filter(pst_id=pk)
        # print(queryset)
        posts = get_list_or_404(queryset,)

        # commentsList = list()
        # for post in posts:
        #     commentsData = dict()
        #     pid = post['pst_id']
        #     comment_queryset = WorkspacePostComment.objects.filter(
        #         post_id=pid).order_by('created_on')
        #     comments = list(comment_queryset)
        #     if not comments:
        #         continue
        #     # comments = get_list_or_404(comment_queryset,)
        #     comment_serializer = WorkspacePostCommentSerializer(
        #         comments, many=True)
        #     commentsList.append(comment_serializer.data)

        post_serializer = PostDataSerializer(posts, many=True)
        # data = dict()
        # for x in posts:
        #     x['comments'] = []
        #     for y in commentsList:
        #         for z in y:
        #             if x['pst_id'] == z['post_id']:
        #                 x['comments'].append(z)
        #             continue
        # data['posts'] = post_serializer.data
        # data['comments'] = commentsList

        return Response(post_serializer.data)


class ProjectPostViewSet(viewsets.ModelViewSet):
    queryset = ProjectPost.objects.all()
    serializer_class = ProjectPostSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        action = pk[0:2]
        pk = pk[2:]
        if action == 'po':  # to search using the project_id
            queryset = ProjectPost.objects.select_related('created_by').values(
                'pst_id', 'pst_content', 'created_on', 'pst_filename', 'pst_filepath', 'created_by__id', 'created_by__first_name', 'created_by__last_name', 'created_by__photo_address', 'created_by__email').filter(project_id=pk).order_by('-created_on')

        elif action == 'ps':  # to search using the post_id
            queryset = ProjectPost.objects.filter(pst_id=pk)
        # print(queryset)
        posts = get_list_or_404(queryset,)
        post_serializer = PostDataSerializer(posts, many=True)

        return Response(post_serializer.data)


class TeamPostViewSet(viewsets.ModelViewSet):
    queryset = TeamPost.objects.all()
    serializer_class = TeamPostSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        action = pk[0]
        pk = pk[1:]
        if action == 't':  # to search using the team_id
            queryset = TeamPost.objects.select_related('created_by').values(
                'pst_id', 'pst_content', 'created_on', 'pst_filename', 'pst_filepath', 'created_by__id', 'created_by__first_name', 'created_by__last_name', 'created_by__photo_address', 'created_by__email').filter(team_id=pk).order_by('-created_on')

        elif action == 'p':  # to search using the post_id
            queryset = TeamPost.objects.filter(pst_id=pk)
        # print(queryset)
        posts = get_list_or_404(queryset,)
        post_serializer = PostDataSerializer(posts, many=True)

        return Response(post_serializer.data)


class WorkspacePostCommentViewSet(viewsets.ModelViewSet):
    queryset = WorkspacePostComment.objects.all()
    serializer_class = WorkspacePostCommentSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        action = pk[0]
        pk = pk[1:]
        if action == 'w':  # to search using the workspace_id
            # cant perform this operation here
            queryset = WorkspacePostComment.objects.filter(workspace_id=pk)

        elif action == 'p':  # to search using the post_id
            queryset = WorkspacePostComment.objects.select_related('created_by').values(
                'c_id', 'c_content', 'created_on', 'created_by__id', 'created_by__first_name', 'created_by__last_name', 'created_by__photo_address').filter(post_id=pk).order_by('created_on')

        try:
            comments = get_list_or_404(queryset,)
        except:
            comments = None

        serializer = PostCommentDataSerializer(comments, many=True)
        return Response(serializer.data)


class ProjectPostCommentViewSet(viewsets.ModelViewSet):
    queryset = ProjectPostComment.objects.all()
    serializer_class = ProjectPostCommentSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        action = pk[0]
        pk = pk[1:]
        if action == 'w':  # to search using the workspace_id
            # cant perform this operation here
            queryset = ProjectPostComment.objects.filter(workspace_id=pk)

        elif action == 'p':  # to search using post_id
            queryset = ProjectPostComment.objects.select_related('created_by').values(
                'c_id', 'c_content', 'created_on', 'created_by__id', 'created_by__first_name', 'created_by__last_name', 'created_by__photo_address').filter(post_id=pk).order_by('created_on')

        try:
            comments = get_list_or_404(queryset,)
        except:
            comments = None

        serializer = PostCommentDataSerializer(comments, many=True)
        return Response(serializer.data)


class TeamPostCommentViewSet(viewsets.ModelViewSet):
    queryset = TeamPostComment.objects.all()
    serializer_class = TeamPostCommentSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        action = pk[0]
        pk = pk[1:]
        if action == 't':  # to search using the team_id
            # cant perform this operation here
            queryset = TeamPostComment.objects.filter(team_id=pk)

        elif action == 'p':  # to search using post_id
            queryset = TeamPostComment.objects.select_related('created_by').values(
                'c_id', 'c_content', 'created_on', 'created_by__id', 'created_by__first_name', 'created_by__last_name', 'created_by__photo_address').filter(post_id=pk).order_by('created_on')

        try:
            comments = get_list_or_404(queryset,)
        except:
            comments = None

        serializer = PostCommentDataSerializer(comments, many=True)
        return Response(serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        action = pk[0]
        pk = pk[1:]
        if action == 'p':  # to search using the project_id
            queryset = Team.objects.filter(project_id=pk)

        elif action == 't':  # to search using the team_id
            queryset = Team.objects.filter(tm_id=pk)

        teams = get_list_or_404(queryset,)
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        action = pk[0:2]
        pk = pk[2:]
        if action == 'tm':  # to search using the team_id
            queryset = Task.objects.filter(team_id=pk)

        elif action == 't':  # to search using the task_id
            queryset = Task.objects.filter(t_id=pk)

        teams = get_list_or_404(queryset,)
        serializer = TaskSerializer(teams, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        action = pk[0]
        pk = pk[1:]
        if action == 'u':  # to search using the user_id
            queryset = Message.objects.select_related('sender_id', 'receiver_id').values(
                'm_id', 'm_content', 'm_filepath', 'created_on', 'sender_id__id', 'sender_id__first_name', 'sender_id__last_name', 'sender_id__photo_address', 'receiver_id__id', 'receiver_id__first_name', 'receiver_id__last_name', 'receiver_id__photo_address').filter(
                Q(sender_id=pk) | Q(receiver_id=pk))
            # queryset = Message.objects.filter(sender_id=pk)

        elif action == 'm':  # to search using the message_id
            queryset = Message.objects.filter(m_id=pk)
        messages = get_list_or_404(queryset,)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class PusherTest():
    pusher_client = pusher.Pusher(
        app_id='960942',
        key='c2c29162a0876ff05eae',
        secret='ccb97a0a4e0f02089327',
        cluster='ap2',
        ssl=True
    )

    pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})

    pusher_client.channels_info(u"my-channel")
