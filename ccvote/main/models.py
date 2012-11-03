import os
import hashlib
from django.db import models

BOOLEAN_CHOICES = (
        (1, 'True'),
        (0, 'False'),
)

USER_STATUS_LOCKED = 'locked'
USER_STATUS_LOGGED_IN = 'logged_in'
USER_STATUS_LOGGED_OUT = 'logged_out'
USER_STATUS_CHOICES = (
        (USER_STATUS_LOCKED, 'Locked'),
        (USER_STATUS_LOGGED_IN, 'Logged in'),
        (USER_STATUS_LOGGED_OUT, 'Logged out'),
)

MOTION_STATUS_CHOICES = (
        ('new', 'New'),
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('withdrawn', 'Withdrawn'),
        ('canceled', 'Canceled'),
)

VOTE_CHOICES = (
        ('pro', 'Pro'),
        ('con', 'Con'),
        ('abstain', 'Abstain'),
)

# Note about BooleanField
#
# A boolean field in MySQL is stored as a TINYINT column with a value of either
# 0 or 1 (most databases have a proper BOOLEAN type instead). So, for MySQL,
# only, when a BooleanField is retrieved from the database and stored on a
# model attribute, it will have the values 1 or 0, rather than True or False.
# Normally, this shouldn't be a problem, since Python guarantees that 1 == True
# and 0 == False are both true. Just be careful if you're writing something
# like obj is True when obj is a value from a boolean attribute on a model. If
# that model was constructed using the mysql backend, the "is" test will fail.
# Prefer an equality test (using "==") in cases like this.

################################################################################
# Create your models here.
class GroupData(models.Model):
    group_id = models.AutoField(
            'Unique group ID number', primary_key=True, db_column='groupID')
    group_name = models.CharField(
            'Group name', max_length=20, unique=True, db_column='groupName')
    group_motion_maint = models.BooleanField(
            'Allowed to maintain motions',
            choices=BOOLEAN_CHOICES, db_column='groupMotionMaint')
    group_run_reports = models.BooleanField(
            'Allowed to run reporting',
            choices=BOOLEAN_CHOICES, db_column='groupRunReports')
    group_voter = models.BooleanField(
            'Allowed to cast votes',
            choices=BOOLEAN_CHOICES, db_column='groupVoter')
    group_admin = models.BooleanField(
            'Allowed to perform admin functions',
            choices=BOOLEAN_CHOICES, db_column='groupAdmin')
    class Meta:
        db_table = u'groupdata'
    def __unicode__(self):
        return self.group_name

class UserData(models.Model):
    user_id = models.AutoField(
            'Unique user ID number', primary_key=True, db_column='userID')
    user_name = models.CharField(
            'User login name', max_length=20, unique=True, db_column='userName')
    user_full_name = models.CharField(
            'User full name', max_length=120, db_column='userFullName')
    # salt is embedded in the field: salt(16) + sha256(64)
    user_pwhash = models.CharField(
            'Password hash', max_length=80, db_column='userPwHash')
    user_status = models.CharField(
            'locked/logged_out/logged_in', max_length=10,
            choices=USER_STATUS_CHOICES, db_column='userStatus')
    user_last_login = models.DateTimeField(
            'Date-time of last login', null=True, db_column='userLastLogin')
    user_last_host = models.CharField(
            'IP of last login', max_length=14, null=True,
            db_column='userLastHost')
    group_id = models.ForeignKey(
            GroupData, verbose_name='Group the user belongs to',
            db_column='groupID')

    def set_password(self, password):
        # SHA256 hash store
        #salt = os.urandom(8)
        hash = hashlib.sha256(password) # +salt
        storage = '%s' % hash.hexdigest() #'%s%s' % (salt.encode('hex'), hash.hexdigest())
        self.user_pwhash = storage
    
    def verify_password(self, password):
        #shex = self.user_pwhash[:16]
        #hash = self.user_pwhash[16:]
        #salt = shex.decode('hex')
        hash = hashlib.sha256(password)
        storage = '%s' % hash.hexdigest()
        if storage == self.user_pwhash:
            return True
        else:
            return False
    
    def status_display(self):
        sd = dict(USER_STATUS_CHOICES)
        return sd[self.user_status]
    
    class Meta:
        db_table = u'userdata'

    def __unicode__(self):
        return self.user_name

class LogData(models.Model):
    log_id = models.AutoField(
            'Action identifier', primary_key=True, db_column='logID')
    user_id = models.ForeignKey(
            UserData, verbose_name='The user taking the action',
            on_delete=models.DO_NOTHING, db_column='userID')
    log_action = models.CharField(
            'The type of action', max_length=20, db_column='logAction')
    details = models.TextField('More information')
    class Meta:
        db_table = u'logdata'
    def __unicode__(self):
        return self.log_id

class MotionData(models.Model):
    motion_id = models.AutoField(
            'Unique motion ID number', primary_key=True, db_column='motionID')
    motion_create_time = models.DateTimeField(
            'Date-time the motion was created', db_column='motionCreateTime', auto_now_add=True)
#    motion_parent = models.IntegerField(
#            'Parent motion (used for recalls)', null=True,
#            db_column='motionParent')
    motion_vote_start = models.DateTimeField(
            'Voting window open time', null=True, db_column='motionVoteStart')
    motion_vote_end = models.DateTimeField(
            'Votin window close time', null=True, db_column='motionVoteEnd')
    motion_clerk_id = models.ForeignKey(
            UserData, verbose_name='Clerk who created the motion',
            db_column='motionClerkID')
    motion_description = models.CharField(
            'Short name or title', max_length=50, db_column='motionDescription')
    motion_comment = models.TextField(
            'Extended comments or notes', db_column='motionComment')
    motion_status = models.CharField(
            'new/open/closed/withdrawn/canceled', max_length=10,
            choices=MOTION_STATUS_CHOICES, db_column='motionStatus')
    class Meta:
        db_table = u'motiondata'
    def __unicode__(self):
        return self.motion_description

class VoteData(models.Model):
    vote_id = models.AutoField(
            'Unique vote ID', primary_key=True, db_column='voteID')
    motion_id = models.ForeignKey(
            MotionData, verbose_name='Motion this vote is on',
            db_column='motionID')
    user_id = models.ForeignKey(
            UserData, verbose_name='User casting the vote', db_column='userID')
    vote_time = models.DateTimeField(
            'Time the vote was cast', db_column='voteTime')
    vote = models.CharField('pro/con/abstain', max_length=10)
    class Meta:
        db_table = u'votedata'
    def __unicode__(self):
        return self.vote

class VoteTemp(models.Model):
    user_id = models.OneToOneField(UserData, related_name="+", primary_key=True)
    user_name = models.OneToOneField(UserData, related_name='+')
    user_status = models.OneToOneField(UserData)
    motion_id = models.ForeignKey(MotionData)
    vote = models.CharField('pro/con/abstain', max_length=10)

# vim: set sts=4 sw=4 expandtab:
