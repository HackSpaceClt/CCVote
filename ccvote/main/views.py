import logging
import datetime
import json
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import simplejson
from main.models import GroupData
from main.models import UserData
from time import sleep
from utils import *
from main.authorization import *

#
# Example view demonstrating template rendering and data access
#
def home(request):
    page_data = {}
    page_data['project_name'] = 'City Council Voting'
    page_data['user_name'] = Security.get_user_name(request)
    page_data['request'] = request
    auth_template_vars(request, page_data)
    return render_to_response('main/home.html', page_data,
                              RequestContext(request))

def videoOverlay(request):
    videoDisplayData = dict()
    voterNames = dict()
    voteCounts = dict()
    visibilityAttrs = dict()
    voteClasses = dict()
    voteClass = str()
    noCount = int()
    yesCount = int()
    for each in VoteTemp.objects.values('user_id').filter(user_id__lt = 13):
        user_id = each['user_id']
        record = VoteTemp.objects.get(user_id = each['user_id'])
        if record.vote == '' or record.user_status == 'logged_out':
            visibilityAttr = 'visibility:hidden'
            voteClass = ''
        else:            
            visibilityAttr = ''
            if str(record.vote) == 'con':
                voteClass = 'noVote'
                noCount += 1
            else:
                voteClass = 'yesVote'
                yesCount += 1
        voterNames.update({user_id:record.user_full_name})
        visibilityAttrs.update({user_id:visibilityAttr + ';'})
        voteClasses.update({user_id:voteClass})
#         'visibilityAttr':visibilityAttr, 'voteClass':voteClass}})
#    voteCounts.update({'yesCount':VoteTemp.objects.filter(vote = 'pro').count()})
#    voteCounts.update({'noCount':VoteTemp.objects.filter(vote = 'con').count()})
    voteCounts.update({'yesCount':yesCount, 'noCount':noCount})
    voteCount = yesCount + noCount
    if voteCount == 0:
        visibilityAttrs.update({'legend':'visibility:hidden;'})
    videoDisplayData['voterNames'] = voterNames
    videoDisplayData['voteCounts'] = voteCounts
    videoDisplayData['visibilityAttrs'] = visibilityAttrs
    videoDisplayData['voteClasses'] = voteClasses
    return render_to_response('main/overlay.html', videoDisplayData, RequestContext(request))

def videoOverlayJson(request):
    '''
    return HttpResponse(str(lastModelChangeTime.objects.values('lastChangeTime').count()))
    '''
    '''
    if lastModelChangeTime.objects.filter(modelName = 'VoteTemp').exists():
        voteTempModelLastChangeTime = lastModelChangeTime.objects.get(modelName = 'VoteTemp').lastChangeTime
    else:
        voteTempModelLastChangeTime = 'empty'
    return HttpResponse(voteTempModelLastChangeTime)
    '''
    '''
    @receiver(main_signals.voteCast)
    def(sender, **kwargs):
    '''
    voteTempRecordsList = []
    for each in VoteTemp.objects.all():
        voteTempRecordDict = {}
        for each2 in each.__dict__:
            if each2 is not '_state':
                voteTempRecordDict.update({each2:each.__dict__[each2]})
        voteTempRecordsList.append(voteTempRecordDict)
    return HttpResponse(json.dumps(voteTempRecordsList))


# Views for vote clients
def VoteClientMinimal(request):
    incoming_data = request.REQUEST
    page_data = {}
    # 'managed_mode' should end up pulling from the DB somewhere...
    page_data['managed_mode'] = '0'
    try:
        page_data['debug'] = incoming_data['debug']
    except:
        page_data['debug'] = '0'
    page_data['user_id'] = Security.get_user_id(request)
    page_data['motion_id'] = MeetingState.get_current_motion().motion_id
    return render_to_response('main/VoteClientMinimal.html', page_data, RequestContext(request))

def VoteClientAjax(request):
    incoming_data = request.REQUEST
    # print "%s %s" % ('new state is', incoming_data['new_state'])
    MeetingState.set_user_vote(incoming_data['motion_id'], incoming_data['user_id'], incoming_data['new_state'])
    response_data = {}
    response_data['result'] = 'test success'
    response_data['message'] = "Server say - dis be what I got from you: %s %s %s" % (
        incoming_data['motion_id'], incoming_data['new_state'], incoming_data['user_id'])
    # this could potentially end up being different based on some conditions/tests here
    response_data['new_state'] = incoming_data['new_state']
    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

def VoteClientAjaxLongPoll(request):
    sleep(30)
    response_data = {}
    response_data['result'] = 'test success'
    response_data['message'] = "%s %s" % ('The world has been Hello-ified as of ', str(datetime.datetime.now()))
    # this will end up coming from the DB or some other coding...
    response_data['new_state'] = "active"
    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

#################
# Views for clerk
#################

# main clerk interface
def ClerkInterface(request):
    incoming_data = request.REQUEST
    image_size_specified = 0
    page_data = {}
    page_data['project_name'] = 'Clerk Interface'
    page_data['user_name'] = Security.get_user_name(request)
    page_data['request'] = request
    page_data['current_meeting_motions'] = MeetingState.get_current_meeting_motions()
    page_data['varname_for'] = "pro"
    page_data['varname_against'] = "con"
    try:
        page_data['copy_just_results'] = incoming_data['copy_just_results']
    except:
        page_data['copy_just_results'] = "0"
    try:
        page_data['ungroup_other_votes'] = incoming_data['ungroup_other_votes']
    except:
        page_data['ungroup_other_votes'] = "0"
    try:
        page_data['debug'] = incoming_data['debug']
    except:
        page_data['debug'] = '0'
    try:
        page_data['image_size'] = incoming_data['image_size']
        image_size_specified = 1
    except:
        page_data['image_size'] = "large"
    try:
        page_data['copy_button_position'] = incoming_data['copy_button_position']
    except:
        page_data['copy_button_position'] = "right"
        if not image_size_specified:
            page_data['image_size'] = "small"
    auth_template_vars(request, page_data)
    return render_to_response('main/clerk.html', page_data, RequestContext(request))

# long poll handler for clerk interface
def ClerkAjaxLongPoll(request):
    sleep(30)
    response_data = {}
    response_data['result'] = 'test success'
    response_data['message'] = "%s %s" % ('The world has been Hello-ified as of ', str(datetime.datetime.now()))
    # this will end up coming from the DB or some other coding...
    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

# ajax handler for clerk requests
def ClerkAjax(request):
    # does nothing yet....
    incoming_data = request.REQUEST
    response_data = {}
    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

# ajax handler for clerk polling of current motions
def ClerkAjaxCurrentMotionIds(request):
    current_motions = MeetingState.get_current_meeting_motions()
    incoming_data = request.REQUEST
    response_data = {}
    response_data['current_motion_ids'] = []
    for motion in current_motions:
        response_data['current_motion_ids'].append(motion.motion_id)
    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

# ajax handler to render insides of each motion
def ClerkAjaxMotionPull(request, motion_id):
    incoming_data = request.REQUEST
    votes_in_motion = MeetingState.get_votes_by_motion_id(motion_id)
    page_data = {}
    page_data['request'] = request
    page_data['motion_id'] = motion_id
    page_data['varname_for'] = "pro"
    page_data['varname_against'] = "con"
    # Commenting as I think it's probably extraneous....
    # page_data['votes_in_motion'] = votes_in_motion
    page_data['voters_for'] = []
    page_data['voters_against'] = []
    page_data['voters_other'] = []
    page_data['motion_description'] = votes_in_motion[0].motion_id.motion_description
    page_data['motion_comment'] = votes_in_motion[0].motion_id.motion_comment
    for vote in filter(lambda x: x.vote == "pro", votes_in_motion):
        page_data['voters_for'].append(vote.user_id.user_full_name)
    for vote in filter(lambda x: x.vote == "con", votes_in_motion):
        page_data['voters_against'].append(vote.user_id.user_full_name)
    try:
        page_data['ungroup_other_votes'] = incoming_data['ungroup_other_votes']
    except:
        page_data['ungroup_other_votes'] = "0"
    if page_data['ungroup_other_votes'] == "0":
        # Append not pro/con votes to the 'for' group but encapsulated
        # in asterisks -- *<name>*
        for vote in filter(lambda x: x.vote != "pro" and x.vote != "con", votes_in_motion):
            page_data['voters_for'].append(''.join(["*", vote.user_id.user_full_name, "*"]))
    else:
        for vote in filter(lambda x: x.vote != "pro" and x.vote != "con", votes_in_motion):
            page_data['voters_other'].append(vote.user_id.user_full_name)
    try:
        page_data['copy_button_position'] = incoming_data['copy_button_position']
    except:
        page_data['copy_button_position'] = "right"
    try:
        page_data['copy_just_results'] = incoming_data['copy_just_results']
    except:
        page_data['copy_just_results'] = "0"
    try:
        page_data['copy_window'] = incoming_data['copy_window']
    except:
        page_data['copy_window'] = "0"
    auth_template_vars(request, page_data)
    return render_to_response('main/clerkajaxmotionpull.html', page_data, RequestContext(request))

def testview(request):
    page_data = {}
    page_data['votes'] = MeetingState.get_current_motion().votedata_set.all()
    return render_to_response('main/testview.html', page_data, RequestContext(request))

def logout(request):
    Security.logout(request)
    return redirect('/')

# vim: set sts=4 sw=4 expandtab:
