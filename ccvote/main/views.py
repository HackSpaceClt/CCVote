import logging
import datetime
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from main.models import GroupData
from main.models import UserData
from time import sleep
from utils import Utils

#
# Example view demonstrating template rendering and data access
#
def home(request):
    page_data = {}
    page_data['project_name'] = 'City Council Voting'
    page_data['datetime'] = datetime.datetime.now()
    page_data['groups'] = GroupData.objects.all()
    page_data['users'] = UserData.objects.all()
    return render_to_response('main/home.html', page_data,
                              RequestContext(request))

def videoOverlay(request):
    videoDisplayData['names']=VoteTemp.objects.values('user_name')
    videoDisplayData['nameAndVote']=VoteTemp.objects.values('user_name').fil
    return render_to_response('main/videoOverlay.html', videoDisplayData, RequestContext(request))

class LoginForm(forms.Form):
    user_name = forms.CharField(label='Login', max_length=20)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    
# Views for vote clients
def VoteClientMinimal(request):
    page_data = {}
    # 'managed_mode' should end up pulling from the DB somewhere...
    page_data['managed_mode'] = '0'
    page_data['debug'] = '1'
    return render_to_response('main/VoteClientMinimal.html', page_data, RequestContext(request))

def VoteClientAjax(request):
    incoming_data = request.REQUEST
    print "%s %s" % ('new state is', incoming_data['new_state'])
    response_data = {}
    response_data['result'] = 'test success'
    response_data['message'] = "%s %s" % ('Server say - dis be what I got from you:', incoming_data['new_state'])
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

#
# Example view demonstrating form handling
#
def login(request):
    page_data = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid() and Utils.validate_user(
                        form.cleaned_data['user_name'],
                        form.cleaned_data['password']):
            # TODO: do login stuff
            logging.info('Login attempt: %s:%s' % 
                         (form.cleaned_data['user_name'],
                          form.cleaned_data['password']))
            return HttpResponseRedirect('/')
        else:
            page_data['error'] = 'Invalid Login'
    else:
        form = LoginForm()
    page_data['form'] = form
    return render_to_response('main/login.html', page_data,
                               RequestContext(request))

# vim: set sts=4 sw=4 expandtab:
