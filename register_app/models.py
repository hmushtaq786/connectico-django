from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class User(AbstractUser):
    status_line = models.CharField(
        max_length=100, verbose_name='Status', blank=True, null=True)
    photo_address = models.CharField(
        max_length=255, blank=True, verbose_name='Photo address', null=True)
    phone_number = models.CharField(
        max_length=20, verbose_name='Phone number', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    org_creator = models.BooleanField(verbose_name='Creator', null=True)
    organization_id = models.ForeignKey(
        'Organization', on_delete=models.CASCADE, null=True, verbose_name='Organization', default='')
    # if user is logged in for the first time, we need to direct him to the page where he must enter his
    # details first
    is_first_login = models.BooleanField(
        verbose_name='First login?', default=True)

    def __str__(self):
        return str(self.id) + ' ' + self.first_name + ' ' + self.last_name


class InvitedUser(models.Model):
    email = models.CharField(max_length=50, verbose_name='Email', blank=True)
    password = models.CharField(
        max_length=50, verbose_name='Password', blank=True)
    organization_id = organization_id = models.ForeignKey(
        'Organization', on_delete=models.CASCADE, null=True, verbose_name='Organization', default='')

    def __str__(self):
        return self.email


class Organization(models.Model):
    name = models.CharField(max_length=30, verbose_name='Organization name')
    website = models.CharField(
        max_length=50, verbose_name='Website', blank=True)
    description = models.TextField(
        verbose_name='Description', blank=True, null=True)
    photo_address = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Photo address')
    address = models.CharField(
        max_length=100, verbose_name='Address', blank=True)
    phone_number = models.CharField(
        max_length=20, verbose_name='Phone number', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, blank=True, unique=True)
    #
    # def created_by_name(self):
    #     user = User.objects.get(id=self.created_by_id)
    #     return user.first_name+" "+user.last_name

    def __str__(self):
        return self.name


class Workspace(models.Model):
    w_id = models.AutoField(primary_key=True)
    w_name = models.CharField(max_length=30, verbose_name='Workspace name')
    description = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='Description')
    w_address = models.CharField(
        max_length=100, verbose_name='Address', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    w_manager_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='workspace_manager')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    organization_id = models.ForeignKey(
        Organization, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.w_name


class Project(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_name = models.CharField(max_length=30, verbose_name='Project name')
    p_description = models.CharField(
        max_length=100, verbose_name='Description', blank=True)
    p_start_date = models.DateField(null=True)
    p_end_date = models.DateField(null=True)
    p_status = models.CharField(
        max_length=10, blank=True, verbose_name='Status')  # completed, active etc
    workspace_id = models.ForeignKey(
        Workspace, null=True, on_delete=models.SET_NULL)
    p_manager_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='project_manager')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='project_creator')

    def __str__(self):
        return self.p_name


class Team(models.Model):
    tm_id = models.AutoField(primary_key=True)
    tm_name = models.CharField(max_length=30, verbose_name='Team name')
    tm_description = models.CharField(
        max_length=100, verbose_name='Description', blank=True)
    tm_start_date = models.DateField()
    tm_end_date = models.DateField()
    project_id = models.ForeignKey(
        Project, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    team_lead_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='team_lead')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.tm_name


class Task(models.Model):

    STATUSES = (
        (0, 'Created'),
        (1, 'Assigned'),
        (2, 'In progress'),
        (3, 'Completed'),
        (4, 'Submitted')
    )

    t_id = models.AutoField(primary_key=True)
    t_name = models.CharField(max_length=30)
    t_description = models.CharField(max_length=100, blank=True)
    t_start_date = models.DateField()
    t_end_date = models.DateField()
    t_status = models.CharField(max_length=10, choices=STATUSES)
    team_id = models.ForeignKey(
        Team, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='created_by')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='assigned_to')

    def __str__(self):
        return self.t_name


class Event(models.Model):
    e_id = models.AutoField(primary_key=True)
    e_name = models.CharField(max_length=30)
    e_description = models.CharField(max_length=100, blank=True)
    e_location = models.CharField(max_length=50, blank=True)
    e_date = models.DateField()
    e_time = models.TimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.e_name


class WorkspaceEvent(Event):
    workspace_id = models.ForeignKey(
        Workspace, null=True, on_delete=models.SET_NULL, related_name='workspace_event_wid')

    def __str__(self):
        return self.e_name


class ProjectEvent(Event):
    project_id = models.ForeignKey(
        Project, null=True, on_delete=models.SET_NULL, related_name='project_event_pid')

    def __str__(self):
        return self.e_name


class TeamEvent(Event):
    team_id = models.ForeignKey(
        Team, null=True, on_delete=models.SET_NULL, related_name='team_event_tid')

    def __str__(self):
        return self.e_name


class Role(models.Model):
    r_id = models.AutoField(primary_key=True)
    r_name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.r_id)+' '+self.r_name


class user_workspace_relation(models.Model):
    uwr_id = models.AutoField(primary_key=True)
    u_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                             on_delete=models.SET_NULL, related_name='workspace_user')
    w_id = models.ForeignKey(
        Workspace, null=True, on_delete=models.SET_NULL, related_name='workspace')
    r_id = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return 'User '+str(self.u_id)+' is in Workspace '+str(self.w_id)


class user_project_relation(models.Model):
    upr_id = models.AutoField(primary_key=True)
    u_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                             on_delete=models.SET_NULL)
    p_id = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL)
    r_id = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return 'User '+str(self.u_id)+' '+str(self.u_id.id)+' is in Project '+str(self.p_id)


class user_team_relation(models.Model):
    utr_id = models.AutoField(primary_key=True)
    u_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                             on_delete=models.SET_NULL)
    t_id = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
    r_id = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return 'User '+str(self.u_id)+' '+str(self.u_id.id)+' is in Team '+str(self.t_id)


class Conversation(models.Model):
    c_id = models.AutoField(primary_key=True)
    channel_name = models.CharField(max_length=50)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='sender')
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='receiver')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.channel_name)


class Message(models.Model):
    m_id = models.AutoField(primary_key=True)
    m_content = models.TextField(verbose_name='Content')
    conversation = models.ForeignKey(
        Conversation, null=True, on_delete=models.SET_NULL)
    sent_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='sent_by')
    # receiver_id = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='receiver')
    created_on = models.DateTimeField(auto_now_add=True)
    # m_filepath = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.conversation.channel_name + " | " + self.m_content


class Notification(models.Model):
    n_id = models.AutoField(primary_key=True)
    n_title = models.CharField(max_length=20)
    n_description = models.CharField(max_length=50, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    n_from = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='n_from')
    n_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='n_to')


class Post(models.Model):
    pst_id = models.AutoField(primary_key=True)
    pst_content = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    pst_filename = models.CharField(
        max_length=30, blank=True, verbose_name='File name', null=True)
    pst_filepath = models.CharField(
        max_length=255, blank=True, verbose_name='File address', null=True)

    def __str__(self):
        return self.created_by.first_name + " -> " + self.pst_content


class WorkspacePost(Post):
    # wp_id = models.AutoField(primary_key=True)
    # post_id = models.ForeignKey(
    #     Post, null=True, on_delete=models.SET_NULL, related_name='workspace_post_pid')
    workspace_id = models.ForeignKey(
        Workspace, null=True, on_delete=models.SET_NULL, related_name='workspace_post_wid')

    def __str__(self):
        return self.created_by.first_name + " -> " + self.pst_content


class ProjectPost(Post):
    project_id = models.ForeignKey(
        Project, null=True, on_delete=models.SET_NULL, related_name='project_post_project_id')


class TeamPost(Post):
    team_id = models.ForeignKey(
        Team, null=True, on_delete=models.SET_NULL, related_name='team_post_tid')


class Comment(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_content = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.created_by.first_name + " -> " + self.c_content


class WorkspacePostComment(Comment):
    post_id = models.ForeignKey(
        WorkspacePost, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.created_by.first_name + " -> " + self.c_content


class ProjectPostComment(Comment):
    post_id = models.ForeignKey(
        ProjectPost, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.created_by.first_name + " -> " + self.c_content


class TeamPostComment(Comment):
    # name = models.CharField(max_length=100, null=True)
    post_id = models.ForeignKey(
        TeamPost, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.created_by.first_name + " -> " + self.c_content
