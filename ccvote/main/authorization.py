# from django.http import Http404
import urllib
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.http import HttpRequest
from django.shortcuts import render_to_response
from django.template import RequestContext
from main.models import GroupData
from main.models import UserData

AUTH_LEVEL_ADMIN    = 1
AUTH_LEVEL_CLERK    = 2
AUTH_LEVEL_REPORTER = 3
AUTH_LEVEL_VOTER    = 4

def authorize_user(user_id, levels):
    """
    Get the group association and test the auth flags
    against the allowed auth levels
    """
    try:
        user = UserData.objects.get(user_id=user_id)
    except ObjectDoesNotExist:
        return False
    group = user.group_id
    for level in levels:
        if level == AUTH_LEVEL_ADMIN:
            if group.group_admin:
                return True
        elif level == AUTH_LEVEL_CLERK:
            if group.group_motion_maint:
                return True
        elif level == AUTH_LEVEL_REPORTER:
            if group.group_run_reports:
                return True
        elif level == AUTH_LEVEL_VOTER:
            if group.group_voter:
                return True
    return False

def _auth_tmpl_vars_false(data):
    data['AUTH_LEVEL_ADMIN'] = False
    data['AUTH_LEVEL_CLERK'] = False
    data['AUTH_LEVEL_REPORTER'] = False
    data['AUTH_LEVEL_VOTER'] = False
    data['LOGGED_IN'] = False

def auth_template_vars(request, data):
    if ('user_id' not in request.session) or (not request.session['user_id']):
        _auth_tmpl_vars_false(data)
        return

    user_id = request.session['user_id']
    try:
        user = UserData.objects.get(user_id=user_id)
    except ObjectDoesNotExist:
        _auth_tmpl_vars_false(data)
        return

    data['LOGGED_IN'] = True

    group = user.group_id
    data['AUTH_LEVEL_ADMIN'] = True if group.group_admin else False
    data['AUTH_LEVEL_CLERK'] = True if group.group_motion_maint else False
    data['AUTH_LEVEL_REPORTER'] = True if group.group_run_reports else False
    data['AUTH_LEVEL_VOTER'] = True if group.group_voter else False

def authorize(*levels):
    def decorator(f):
        def aux(*args):
            #
            # Let's figure out what we're authorizing
            #
            if len(args) == 0:
                raise Exception('Invalid use of authorize()')

            if isinstance(args[0], HttpRequest):
                # Normal view.  args[0] is the request
                request = args[0]
            elif hasattr(args[0], 'request'):
                # Action view.  args[0] is self
                request = args[0].request
            else:
                raise Exception('Invalid use of authorize()')

            #
            # Check if authenticated
            #
            if not request.session.get('user_id'):
                params = dict(ref=request.path)
                return redirect('/login?%s' % urllib.urlencode(params))

            user_id = request.session['user_id']

            #
            # Check auth
            #
            if not authorize_user(user_id, levels):
                # Could happen if user's permissions are
                # modified during a session
                return user_not_authorized(request)

            #
            # User is ok.  Allow the view action.
            #
            return f(*args)
        return aux
    return decorator

def user_not_authorized(request):
    page_data = {}
    auth_template_vars(request, page_data)
    return render_to_response('main/unauthorized.html', page_data,
                              RequestContext(request))

# vim: set sts=4 sw=4 expandtab:
