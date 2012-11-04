import datetime
from django import forms
from django.http import Http404
from django.utils.log import getLogger
from main import models
from main.utils import ActionView
from main.utils import Security
from main.models import GroupData
from main.models import UserData

logger = getLogger('debugging')

class LoginForm(forms.Form):
    ref = forms.CharField(widget=forms.HiddenInput, required=False)
    user_name = forms.CharField(label='Login', max_length=20)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class UserLogin(ActionView):
    
    def prompt_form(self, form):
        self.data['form'] = form
        return self.render_html('main/login.html')

    def action_login(self, args):
        form = LoginForm(args)
        if not form.is_valid():
            self.data['error'] = 'Errors'
            return self.prompt_form(form)

        d = form.cleaned_data
        user_name = d['user_name'].encode('utf8')
        password = d['password'].encode('utf8')
        if not Security.login(self.request, user_name, password):
            self.data['error'] = 'Username or password error'
            return self.prompt_form(form)
        ref = d['ref'] if d['ref'] else '/'
        return self.redirect(ref)

    def action(self, args):
        ref = args['ref'] if 'ref' in args else '/'
        form = LoginForm(initial={'ref': ref})
        return self.prompt_form(form)

    def default(self):
        form = LoginForm()
        return self.prompt_form(form)

# vim: set sts=4 sw=4 expandtab:
