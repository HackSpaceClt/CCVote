import logging
import datetime
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
    videoDisplayData = {}
    videoDisplayData['names'] = VoteTemp.objects.values('user_name')
    videoDisplayData['nameAndVote'] = VoteTemp.objects.values('user_name').fil
    return render_to_response('main/videoOverlay.html', videoDisplayData, RequestContext(request))

# Views for vote clients
def VoteClientMinimal(request):
    page_data = {}
    # 'managed_mode' should end up pulling from the DB somewhere...
    page_data['managed_mode'] = '0'
    page_data['debug'] = '1'
    page_data['user_id'] = Security.get_user_id(request)
    page_data['motion_id'] = MeetingState.get_current_motion().motion_id
    return render_to_response('main/VoteClientMinimal.html', page_data, RequestContext(request))

def VoteClientAjax(request):
    incoming_data = request.REQUEST
    print "%s %s" % ('new state is', incoming_data['new_state'])

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

def logout(request):
    Security.logout(request)
    return redirect('/')

# vim: set sts=4 sw=4 expandtab:
