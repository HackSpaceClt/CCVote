from django.contrib import admin
from main.models import GroupData
from main.models import UserData
from main.models import LogData
from main.models import MotionData
from main.models import VoteData

class GroupsAdmin(admin.ModelAdmin):
    list_display = ('group_name',
                    'group_motion_maint',
                    'group_run_reports',
                    'group_voter',
                    'group_admin')

class UsersAdmin(admin.ModelAdmin):
    fields = ['user_name',
              'user_first_name',
              'user_last_name',
              'user_status',
              'group_id']
    list_display = ('user_name',
                    'user_first_name',
                    'user_last_name',
                    'user_status',
                    'user_last_login',
                    'user_last_host',
                    'group_id')

class LogAdmin(admin.ModelAdmin):
    list_display = ('log_action',
                    'user_id',
                    'details')

class MotionsAdmin(admin.ModelAdmin):
    list_display = ('motion_description',
                    'motion_status',
                    'motion_clerk_id',
                    'motion_create_time',
                    'motion_parent',
                    'motion_vote_start',
                    'motion_vote_end')

class VotesAdmin(admin.ModelAdmin):
    list_display = ('motion_id',
                    'user_id',
                    'vote_time',
                    'vote')

admin.site.register(GroupData, GroupsAdmin)
admin.site.register(UserData, UsersAdmin)
admin.site.register(LogData)
admin.site.register(MotionData)
admin.site.register(VoteData)

# vim: set sts=4 sw=4 expandtab:
