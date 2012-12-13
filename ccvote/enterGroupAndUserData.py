import time
from main.models import *

# set vote_cycle to the number of seconds you want to delay before each cycle of votes is entered (use 0 for no delay):
vote_cycle = 1

def vote_delay(vote_cycle):
    time.sleep(vote_cycle)

p = GroupData(group_id=1, group_name='member')
p.save()
p = GroupData(group_id=2, group_name='Mayor')
p.save()
p = GroupData(group_id=3, group_name='clerk')
p.save()

p = UserData(user_name='jautry', user_full_name='John Autry', user_first_name='John', user_last_name='Autry', user_status='logged_in', group_id=GroupData.objects.get(group_id=1))
p.save()
p = UserData(user_name='mbarnes', user_full_name='Michael Barnes', user_first_name='Michael', user_last_name='Barnes', user_status='logged_in', group_id=GroupData.objects.get(group_id=1))
p.save()
p = UserData(user_name='pcannon', user_full_name='Patrick Cannon', user_first_name='Patrick', user_last_name='Cannon', user_status='logged_in', group_id=GroupData.objects.get(group_id=1))
p.save()
p = UserData(user_name='wcooksey', user_full_name='Warren Cooksey', user_first_name='Warren', user_last_name='Cooksey', user_status='logged_in', group_id=GroupData.objects.get(group_id=1))
p.save()
p = UserData(user_name='adulin', user_full_name='Andy Dulin', user_first_name='Andy', user_last_name='Dulin', user_status='logged_in', group_id=GroupData.objects.get(group_id=1))
p.save()
p = UserData(user_name='cfallon', user_full_name='Claire Fallon', user_first_name='Claire', user_last_name='Fallon', user_status='logged_in', group_id=GroupData.objects.get(group_id=1))
p.save()
p = UserData(user_name='dhoward', user_full_name='David Howard', user_first_name='David', user_last_name='Howard', user_status='logged_in', group_id=GroupData.objects.get(group_id=1))
p.save()
p = UserData(user_name='pkinsey', user_full_name='Patsy Kinsey', user_first_name='Patsy', user_last_name='Kinsey', user_status='logged_in', group_id=GroupData.objects.get(group_id=1))
p.save()
p = UserData(user_name='lmayfield', user_full_name='LaWana Mayfield', user_first_name='LaWana', user_last_name='Mayfield', user_status='logged_in', group_id=GroupData.objects.get(group_id=1))
p.save()
p = UserData(user_name='jmitchell', user_full_name='James Mitchell', user_first_name='James', user_last_name='Mitchell', user_status='logged_in', group_id=GroupData.objects.get(group_id=1))
p.save()
p = UserData(user_name='bpickering', user_full_name='Beth Pickering', user_first_name='Beth', user_last_name='Pickering', user_status='logged_in', group_id=GroupData.objects.get(group_id=1))
p.save()
p = UserData(user_name='afox', user_full_name='Anthony Fox', user_first_name='Anthony', user_last_name='Fox', user_status='logged_in', group_id=GroupData.objects.get(group_id=2))
p.save()
p = UserData(user_name='aprice', user_full_name='Ashley Price', user_first_name='Ashley', user_last_name='Price', user_status='logged_in', group_id=GroupData.objects.get(group_id=3))
p.save()


