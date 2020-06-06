from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, OrganizationViewSet, ProjectViewSet, OrganizationUsersViewSet, WorkspaceViewSet, WorkspaceMembersViewSet, InviteMembers, OrganizationInvitedUserViewSet, FirstTimeUserAuth, UserWorkspaceRelationViewSet, UserProjectRelationViewSet, EventViewSet, WorkspaceEventViewSet, PostViewSet, WorkspacePostViewSet, WorkspacePostCommentViewSet, UserProjectViewSet, TeamViewSet, ProjectEventViewSet
from django.contrib.auth.forms import UserCreationForm


router = routers.DefaultRouter()
router.register('users', UserViewSet, base_name='User')
router.register('organizations', OrganizationViewSet)
router.register('organization/members', OrganizationUsersViewSet)
router.register('organization/workspaces/posts', WorkspacePostViewSet)
router.register('organization/workspaces/comments',
                WorkspacePostCommentViewSet)
router.register('organization/workspaces/projects', ProjectViewSet)
router.register('organization/workspaces/teams', TeamViewSet)
router.register('organization/users/projects', UserProjectViewSet)
router.register('organization/workspaces/members',
                WorkspaceMembersViewSet, base_name='workspace_members')
router.register('organization/workspaces', WorkspaceViewSet)
# router.register('organization/projects', WorkspaceViewSet)
router.register('posts', PostViewSet)

router.register('organizations', OrganizationViewSet)
router.register('organization/events/workspace', WorkspaceEventViewSet)
router.register('organization/events/project', ProjectEventViewSet)
router.register('organization/events', EventViewSet)
router.register('organization/invites', OrganizationInvitedUserViewSet)
router.register('organization/workspace/add', UserWorkspaceRelationViewSet)
router.register('organization/project/add', UserProjectRelationViewSet)

# router.register('users/auth', FirstTimeUserAuth)
# router.register('invite', InviteMembers, basename='Invite')

urlpatterns = [
    path('', include(router.urls)),
    path('invite', InviteMembers.as_view()),
    path('authenticate', FirstTimeUserAuth.as_view())
]
