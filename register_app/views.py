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
from .models import Organization, Workspace, Project, Team, InvitedUser
from .serializers import UserSerializer, OrganizationSerializer, UserMiniSerializer, WorkspaceSerializer, ProjectSerializer, TeamSerializer, InvitedUserSerializer
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from django.contrib.auth.hashers import make_password

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    authentication_classes = (BasicAuthentication,)

    def create(self, request):
        print('create')
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
            print(request.method)
            _mutable = request.data._mutable
            request.data._mutable = True
            user = get_user_model().objects.create(
                email=request.data['email'],
                username=request.data['username'],
                password=make_password(request.data['password']),
                first_name=request.data['first_name'],
                last_name=request.data['last_name'],
                status_line=request.data.setdefault('status_line', ''),
                phone_number=request.data.setdefault('phone_number', ''),
                photo_address=request.data.setdefault('photo_address', ''))

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

    def retrieve(self, request, pk=None):
        # lookup_value_regex = '[\w.]+'
        queryset = Organization.objects.filter(created_by=pk)
        organization = get_object_or_404(queryset,)
        serializer = OrganizationSerializer(organization)
        return Response(serializer.data)


class OrganizationUsersViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserMiniSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        queryset = get_user_model().objects.filter(organization_id=pk)
        print(queryset)
        users = get_list_or_404(queryset,)
        print(users)
        serializer = UserMiniSerializer(users, many=True)
        print(serializer)
        print(serializer.data)
        return Response(serializer.data)


class OrganizationWorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        queryset = Workspace.objects.filter(organization_id=pk)
        print(queryset)
        workspaces = get_list_or_404(queryset,)
        serializer = WorkspaceSerializer(workspaces, many=True)
        print(serializer)
        print(serializer.data)
        return Response(serializer.data)


class OrganizationProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.select_related('workspace_id', '')
    serializer_class = ProjectSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        queryset = Project.objects.filter(organization_id=pk)
        print(queryset)
        workspaces = get_list_or_404(queryset,)
        serializer = WorkspaceSerializer(workspaces, many=True)
        print(serializer)
        print(serializer.data)
        return Response(serializer.data)


class OrganizationInvitedUserViewSet(viewsets.ModelViewSet):
    queryset = InvitedUser.objects.all()
    serializer_class = InvitedUserSerializer
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        queryset = InvitedUser.objects.filter(organization_id=pk)
        print(queryset)
        invited_users = get_list_or_404(queryset,)
        serializer = InvitedUserSerializer(invited_users, many=True)
        print(serializer)
        print(serializer.data)
        return Response(serializer.data)


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
                    'no-reply@connectico.com',
                    [email],
                    fail_silently=False,
                )
                valid_emails.append(email)
            else:
                print('Discarded', email)

        return Response(valid_emails)
