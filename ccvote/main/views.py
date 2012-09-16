import datetime
from django.shortcuts import render_to_response
from main.models import GroupData
from main.models import UserData

# Example view demonstrating template rendering and data access
def home(request):
    page_data = {}
    page_data['project_name'] = 'City Council Voting'
    page_data['datetime'] = datetime.datetime.now()
    page_data['groups'] = GroupData.objects.all()
    page_data['users'] = UserData.objects.all()
    return render_to_response('main/home.html', page_data)
