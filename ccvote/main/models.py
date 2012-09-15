from django.db import models

# Create your models here.
class GroupData(models.Model):
    groupid = models.BigIntegerField(primary_key=True, db_column='groupID')
    groupname = models.CharField(max_length=60, db_column='groupName')
    groupmotionmaint = models.IntegerField(db_column='groupMotionMaint')
    grouprunreports = models.IntegerField(db_column='groupRunReports')
    groupvoter = models.IntegerField(db_column='groupVoter')
    groupadmin = models.IntegerField(db_column='groupAdmin')
    class Meta:
        db_table = u'groupdata'

class UserData(models.Model):
    userid = models.BigIntegerField(primary_key=True, db_column='userID')
    username = models.CharField(max_length=60, db_column='userName')
    userfullname = models.CharField(max_length=360, db_column='userFullName')
    userpwhash = models.CharField(max_length=240, db_column='userPwHash')
    userstatus = models.CharField(max_length=30, db_column='userStatus')
    userlastlogin = models.DateTimeField(db_column='userLastLogin')
    userlasthost = models.CharField(max_length=42, db_column='userLastHost')
    groupid = models.ForeignKey(GroupData, db_column='groupID')
    class Meta:
        db_table = u'userdata'

class LogData(models.Model):
    logid = models.BigIntegerField(primary_key=True, db_column='logID')
    userid = models.ForeignKey(UserData, db_column='userID')
    logaction = models.CharField(max_length=60, db_column='logAction')
    details = models.TextField()
    class Meta:
        db_table = u'logdata'

class MotionData(models.Model):
    motionid = models.BigIntegerField(primary_key=True, db_column='motionID')
    motioncreatetime = models.DateTimeField(db_column='motionCreateTime')
    motionparent = models.BigIntegerField(db_column='motionParent')
    motionvotestart = models.DateTimeField(db_column='motionVoteStart')
    motionvoteend = models.DateTimeField(db_column='motionVoteEnd')
    motionclerkid = models.ForeignKey(UserData, db_column='motionClerkID')
    motiondescription = models.CharField(max_length=150, db_column='motionDescription')
    motioncomment = models.TextField(db_column='motionComment')
    motionstatus = models.CharField(max_length=30, db_column='motionStatus')
    class Meta:
        db_table = u'motiondata'

class VoteData(models.Model):
    voteid = models.BigIntegerField(primary_key=True, db_column='voteID')
    motionid = models.ForeignKey(MotionData, db_column='motionID')
    userid = models.ForeignKey(UserData, db_column='userID')
    votetime = models.DateTimeField(db_column='voteTime')
    vote = models.CharField(max_length=30)
    class Meta:
        db_table = u'votedata'


