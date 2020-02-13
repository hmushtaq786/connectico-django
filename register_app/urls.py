from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, OrganizationViewSet, OrganizationUsersViewSet

from django.contrib.auth.forms import UserCreationForm



router = routers.DefaultRouter()
router.register('users', UserViewSet, base_name='User')
router.register('organizations', OrganizationViewSet)
router.register('members', OrganizationUsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
