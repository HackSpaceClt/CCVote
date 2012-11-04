from django import forms
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.utils.log import getLogger
from main.utils import ActionView
from main.utils import BoolSelect
from main.models import GroupData
from main.models import UserData
from main.authorization import *

logger = getLogger('debugging')

class GroupForm(forms.ModelForm):
    class Meta:
        model = GroupData
        widgets = {
            'group_motion_maint': BoolSelect(),
            'group_run_reports': BoolSelect(),
            'group_voter': BoolSelect(),
            'group_admin': BoolSelect(),
        }

class GroupName(forms.Form):
    group_name = forms.CharField()

class GroupControllerBase(ActionView):

    def get_group_name(self, args):
        id_form = GroupName(args)
        if not id_form.is_valid():
            # invalid url data somehow.. punt
            raise Http404

        # TODO: insert group_name validation
        #       if we don't have a record by 
        #       that name then punt (404)

        # NOTE: May want a specialized "group not found"
        return id_form.cleaned_data['group_name']

class GroupDetails(GroupControllerBase):
    
    @authorize(AUTH_LEVEL_ADMIN)
    def action(self, args):
        group_name = self.get_group_name(args)
        try:
            group = GroupData.objects.get(group_name=group_name)
        except ObjectDoesNotExist:
            raise Http404
        # TODO: Get members
        members = UserData.objects.filter(group_id=group.group_id)
        self.data['members'] = members
        self.data['group'] = group
        return self.render_html('main/group.html')

class GroupCreate(ActionView):
    
    def prompt_form(self, form):
        self.data['form'] = form
        return self.render_html('main/group-create.html')

    @authorize(AUTH_LEVEL_ADMIN)
    def action_save(self, args):
        form = GroupForm(args)
        if not form.is_valid():
            self.data['error_message'] = 'Errors'
            return self.prompt_form(form)

        form.save()
        return self.redirect('/groups')

    @authorize(AUTH_LEVEL_ADMIN)
    def default(self):
        form = GroupForm()
        return self.prompt_form(form)

class GroupEdit(GroupControllerBase):

    def prompt_form(self, form):
        self.data['form'] = form
        return self.render_html('main/group-edit.html')

    @authorize(AUTH_LEVEL_ADMIN)
    def action_save(self, args):
        # Get the group to *update*
        group_name = self.get_group_name(args)
        group = GroupData.objects.get(group_name=group_name)
        self.data['group_name'] = group_name

        # bind form data against the pre-existing group
        form = GroupForm(args, instance=group)
        if not form.is_valid():
            self.data['error_message'] = 'Errors'
            return self.prompt_form(form)

        updated_group = form.save(commit=False)
        # verify stuff...
        # TODO: Log action
        updated_group.save()
        # TODO: recover from exceptions
        return self.redirect('/group/%s' % updated_group.group_name)
    
    @authorize(AUTH_LEVEL_ADMIN)
    def action(self, args):
        group_name = self.get_group_name(args)
        group = GroupData.objects.get(group_name=group_name)
        self.data['group_name'] = group
        form = GroupForm(instance=group)
        return self.prompt_form(form)

class GroupListing(GroupControllerBase):

    @authorize(AUTH_LEVEL_ADMIN)
    def action(self, args):
        groups_all = GroupData.objects.all()
        paginator = Paginator(groups_all, 25)
        
        page_no = args.get('page')
        try:
            groups = paginator.page(page_no)
        except PageNotAnInteger:
            groups = paginator.page(1)
        except EmptyPage:
            groups = paginator.page(paginator.num_pages)

        self.data['groups'] = groups
        return self.render_html('main/groups.html')
    
    @authorize(AUTH_LEVEL_ADMIN)
    def default(self):
        groups_all = GroupData.objects.all()
        paginator = Paginator(groups_all, 25)
        groups = paginator.page(1)
        self.data['groups'] = groups
        return self.render_html('main/groups.html')

# vim: set sts=4 sw=4 expandtab:
