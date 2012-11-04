from django import forms
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.core.validators import validate_slug
from django.utils.log import getLogger
from main.utils import ActionView
from main.utils import BoolSelect
from main import models
from main.models import GroupData
from main.models import UserData
from main.models import USER_STATUS_CHOICES
from main.authorization import *

logger = getLogger('debugging')

# Just using a regular form here
class UserForm(forms.Form):
    user_name = forms.CharField(
            max_length=20, validators=[validate_slug], required=True)
    user_full_name = forms.CharField(max_length=100, required=True)
    user_password = forms.CharField(
            max_length=100, widget=forms.PasswordInput, required=True)
    user_password_confirm = forms.CharField(
            max_length=100, widget=forms.PasswordInput, required=True)
    group_id = forms.ModelChoiceField(
            GroupData.objects.all(), required=True)

# Using a different form to allow password update to be optional
class UserFormEdit(forms.Form):
    user_name = forms.CharField(
            max_length=20, validators=[validate_slug], required=True)
    user_full_name = forms.CharField(max_length=100, required=True)
    group_id = forms.ModelChoiceField(
            GroupData.objects.all(), required=True)
    user_password = forms.CharField(
            max_length=100, widget=forms.PasswordInput, required=False)
    user_password_confirm = forms.CharField(
            max_length=100, widget=forms.PasswordInput, required=False)


class UserName(forms.Form):
    user_name = forms.CharField()

class UserControllerBase(ActionView):

    def get_user_name(self, args):
        id_form = UserName(args)
        if not id_form.is_valid():
            # invalid url data somehow.. punt
            raise Http404

        # TODO: insert user_name validation
        #       if we don't have a record by 
        #       that name then punt (404)

        # NOTE: May want a specialized "user not found"
        return id_form.cleaned_data['user_name']

    def get_user_rec(self, args):
        user_name = self.get_user_name(args)
        try:
            user = UserData.objects.get(user_name=user_name)
        except ObjectDoesNotExist:
            raise Http404
        return user

class UserDetails(UserControllerBase):
    
    @authorize(AUTH_LEVEL_ADMIN)
    def action(self, args):
        self.data['usr'] = self.get_user_rec(args)
        return self.render_html('main/user.html')

class UserDeleteConfirm(UserControllerBase):

    @authorize(AUTH_LEVEL_ADMIN)
    def action_delete(self, args):
        user = self.get_user_rec(args)
        # TODO: make a transaction and log it in LogData
        # FIXME: Deactivate vs. delete in order to 
        #        data integrity (LogData VoteData, etc)
        user.delete()
        return self.redirect('/users/')
    
    @authorize(AUTH_LEVEL_ADMIN)
    def action(self, args):
        self.data['usr'] = self.get_user_rec(args)
        return self.render_html('main/user-delete.html')

class UserCreate(ActionView):
    
    def prompt_form(self, form):
        self.data['form'] = form
        return self.render_html('main/user-create.html')

    @authorize(AUTH_LEVEL_ADMIN)
    def action_save(self, args):
        form = UserForm(args)
        if not form.is_valid():
            self.data['error_message'] = 'Errors'
            return self.prompt_form(form)

        d = form.cleaned_data
        if d['user_password'] != d['user_password_confirm']:
            self.data['error_message'] = 'Password typo'
            return self.prompt_form(form)

        new_user = UserData(user_name=d['user_name'],
                            user_full_name=d['user_full_name'],
                            user_status=models.USER_STATUS_LOGGED_OUT,
                            group_id=d['group_id'])
        new_user.set_password(d['user_password'].encode('utf8'))
        # TODO: log actions in LogData
        new_user.save()
        return self.redirect('/users')

    @authorize(AUTH_LEVEL_ADMIN)
    def default(self):
        form = UserForm()
        return self.prompt_form(form)

class UserEdit(UserControllerBase):

    def prompt_form(self, form):
        self.data['form'] = form
        return self.render_html('main/user-edit.html')

    @authorize(AUTH_LEVEL_ADMIN)
    def action_save(self, args):
        user = self.get_user_rec(args)
        self.data['user_name'] = user.user_name

        # bind form data against the pre-existing user
        form = UserFormEdit(args)
        if not form.is_valid():
            self.data['error_message'] = 'Errors'
            return self.prompt_form(form)

        d = form.cleaned_data
        if d['user_password'] or d['user_password_confirm']:
            change_password = True
            if d['user_password'] != d['user_password_confirm']:
                self.data['error_message'] = 'Password typo'
                return self.prompt_form(form)
        else:
            change_password = False

        user.user_name = d['user_name']
        user.user_full_name = d['user_full_name']
        if change_password:
            user.set_password(d['user_password'].encode('utf8'))
        user.group_id = d['group_id']
        # verify stuff...
        # TODO: Log action
        user.save()
        # TODO: recover from exceptions
        return self.redirect('/user/%s' % user.user_name)
    
    @authorize(AUTH_LEVEL_ADMIN)
    def action(self, args):
        user = self.get_user_rec(args)
        self.data['user_name'] = user.user_name

        # WTF: I kind of want to stab my eyes out because of this.
        #      Does form initialization have to be *this* 
        #      complicated?
        # look into http://djangosnippets.org/snippets/199/
        initial = dict(user.__dict__)
        initial['group_id'] = user.group_id._get_pk_val() # really... really?
        form = UserFormEdit(initial=initial)

        return self.prompt_form(form)

class UserListing(UserControllerBase):

    @authorize(AUTH_LEVEL_ADMIN)
    def action(self, args):
        users_all = UserData.objects.all()
        paginator = Paginator(users_all, 25)
        
        page_no = args.get('page')
        try:
            users = paginator.page(page_no)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        self.data['users'] = users
        return self.render_html('main/users.html')
    
    @authorize(AUTH_LEVEL_ADMIN)
    def default(self):
        users_all = UserData.objects.all()
        paginator = Paginator(users_all, 25)
        users = paginator.page(1)
        self.data['users'] = users
        return self.render_html('main/users.html')

# # vim: set sts=4 sw=4 expandtab:
