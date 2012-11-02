from main.models import *

for each in range(1,13):
    p = VoteTemp(motion_id = MotionData.objects.get(motion_id = 1), user_id = UserData.objects.get(user_id = each), user_name = UserData.objects.get(user_id = each), user_status = UserData.objects.get(user_id = each), vote = 'pro')
    p.save()


