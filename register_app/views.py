from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from .models import Organization, Workspace
from .serializers import UserSerializer, OrganizationSerializer, UserMiniSerializer, WorkspaceSerializer
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
