from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, OrganizationViewSet, OrganizationUsersViewSet, OrganizationWorkspaceViewSet, invite, InviteMembers
from django.contrib.auth.forms import UserCreationForm


router = routers.DefaultRouter()
router.register('users', UserViewSet, base_name='User')
router.register('organizations', OrganizationViewSet)
router.register('organization/members', OrganizationUsersViewSet)
router.register('organization/workspaces', OrganizationWorkspaceViewSet)
router.register('organization/projects', OrganizationWorkspaceViewSet)
# router.register('invite', InviteMembers, basename='Invite')

urlpatterns = [
    path('', include(router.urls)),
    path('invite', InviteMembers.as_view()),
]
