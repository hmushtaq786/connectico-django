from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, OrganizationViewSet, OrganizationUsersViewSet, OrganizationWorkspaceViewSet
from django.contrib.auth.forms import UserCreationForm


router = routers.DefaultRouter()
router.register('users', UserViewSet, base_name='User')
router.register('organizations', OrganizationViewSet)
router.register('organization/members', OrganizationUsersViewSet)
router.register('organization/workspaces', OrganizationWorkspaceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
