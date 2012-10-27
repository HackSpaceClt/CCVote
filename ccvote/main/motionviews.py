from django import forms
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.utils.log import getLogger
from main.utils import ActionView
from main.utils import BoolSelect
from main.models import MotionData
from main.models import UserData

logger = getLogger('debugging')

#class MotionsView(ActionView):
#	def default(self):
#		self.data["myvar"] = "Hi there!"
#		return self.render_html("main/motion.html")

logger = getLogger('debugging')

class MotionForm(forms.ModelForm):
    class Meta:
        model = MotionData
        widgets = {
            'motion_motion_maint': BoolSelect(),
            'motion_run_reports': BoolSelect(),
            'motion_voter': BoolSelect(),
            'motion_admin': BoolSelect(),
        }

class MotionId(forms.Form):
    motion_id = forms.CharField()

class MotionControllerBase(ActionView):

    def get_motion_id(self, args):
        id_form = MotionName(args)
        if not id_form.is_valid():
            # invalid url data somehow.. punt
            raise Http404

        # TODO: insert motion_name validation
        #       if we don't have a record by 
        #       that name then punt (404)

        # NOTE: May want a specialized "motion not found"
        return id_form.cleaned_data['motion_id']

class MotionDetails(MotionControllerBase):
    
    def action(self, args):
        motion_name = self.get_motion_id(args)
        try:
            motion = MotionData.objects.get(motion_id=motion_id)
        except ObjectDoesNotExist:
            raise Http404
        # TODO: Get members
        members = UserData.objects.filter(motion_id=motion.motion_id)
        self.data['members'] = members
        self.data['motion'] = motion
        return self.render_html('main/motion.html')

class MotionCreate(ActionView):
    
    def prompt_form(self, form):
        self.data['form'] = form
        return self.render_html('main/motion-create.html')

    def action_save(self, args):
        form = MotionForm(args)
        if not form.is_valid():
            self.data['error_message'] = 'Errors'
            return self.prompt_form(form)

        form.save()
        return self.redirect('/motions')

    def default(self):
        form = MotionForm()
        return self.prompt_form(form)

class MotionEdit(MotionControllerBase):

    def prompt_form(self, form):
        self.data['form'] = form
        return self.render_html('main/motion-edit.html')

    def action_save(self, args):
        # Get the motion to *update*
        motion_name = self.get_motion_id(args)
        motion = MotionData.objects.get(motion_id=motion_id)
        self.data['motion_name'] = motion_name

        # bind form data against the pre-existing motion
        form = MotionForm(args, instance=motion)
        if not form.is_valid():
            self.data['error_message'] = 'Errors'
            return self.prompt_form(form)

        updated_motion = form.save(commit=False)
        # verify stuff...
        # TODO: Log action
        updated_motion.save()
        # TODO: recover from exceptions
        return self.redirect('/motion/%s' % updated_motion.motion_name)
    
    def action(self, args):
        motion_id = self.get_motion_id(args)
        motion = MotionData.objects.get(motion_id=motion_id)
        self.data['motion_id'] = motion
        form = MotionForm(instance=motion)
        return self.prompt_form(form)

class MotionListing(MotionControllerBase):

    def action(self, args):
        motions_all = MotionData.objects.all()
        paginator = Paginator(motions_all, 25)
        
        page_no = args.get('page')
        try:
            motions = paginator.page(page_no)
        except PageNotAnInteger:
            motions = paginator.page(1)
        except EmptyPage:
            motions = paginator.page(paginator.num_pages)

        self.data['motions'] = motions
        return self.render_html('main/motions.html')
    
    def default(self):
        motions_all = MotionData.objects.all()
        paginator = Paginator(motions_all, 25)
        motions = paginator.page(1)
        self.data['motions'] = motions
        return self.render_html('main/motions.html')
