from main.models import *
from main.utils import *
import random, threading, time
from main import main_signals
from django.dispatch import receiver
import datetime
import json

class VoteOpener:
    def open_vote(self, motion_idArg):
        main_signals.vote_open_signal.send(sender=self, motion_id=motion_idArg)

class VoteCloser:
    def close_vote(self, motion_idArg):
        main_signals.vote_close_signal.send(sender=self, motion_id=motion_idArg)

class VoteCaster:
    def cast_vote(self, motion_idArg, user_idArg, voteArg):
        main_signals.vote_cast_signal.send(sender=self, motion_id=motion_idArg, user_id=user_idArg, vote=voteArg)

@receiver(main_signals.vote_open_signal)
def open_vote(sender, **kwargs):
    p = MotionData.objects.get(motion_id = kwargs['motion_id'])
    p.motion_vote_start = datetime.datetime.utcnow()
    p.save()

@receiver(main_signals.vote_close_signal)
def close_vote(sender, **kwargs):
    p = MotionData.objects.get(motion_id = kwargs['motion_id'])
    p.motion_vote_end = datetime.datetime.utcnow()
    p.save()

@receiver(main_signals.vote_cast_signal)
def save_vote(sender, **kwargs):
    MeetingState.set_user_vote(kwargs['motion_id'], kwargs['user_id'], kwargs['vote'])

vote_opener = VoteOpener()
vote_closer = VoteCloser()
vote_caster = VoteCaster()

def send_random_vote_cast_signals():
    for count in range(1,6):
        p = MotionData(motion_id=count, motion_clerk_id=UserData.objects.get(user_id=13))
        p.save()
        motion_id = count
        vote_opener.open_vote(motion_id)
        time.sleep(5)
        random_user_id_list = []
        yesCount=0
        noCount=0
#        motion_id = MeetingState.get_current_motion().motion_id
        x=1
        while x<12:
            random_user_id = random.randint(1,12)
            if (random_user_id not in random_user_id_list):
                a = random.random()
                if a < 0.5 and yesCount < 9:
                    if random_user_id != 12 or a < 0.15:
                        vote = 'pro'
                        yesCount+=1
                        random_user_id_list.append(random_user_id)
                        vote_caster.cast_vote(motion_id, random_user_id, vote)
                        x+=1
                elif noCount<9:
                    if random_user_id != 12 or a < 0.15:
                        vote = 'con'
                        noCount+=1
                        random_user_id_list.append(random_user_id)
                        vote_caster.cast_vote(motion_id, random_user_id, vote)
                        x+=1
#                vote_caster.cast_vote(motion_idArg=motion_id, user_idArg=random_user_id, voteArg=vote)
                b = random.random()
                b *= 0.4
                time.sleep(b)
        vote_closer.close_vote(motion_id)
        time.sleep(7)

MotionData.objects.all().delete()
VoteData.objects.all().delete()
send_random_vote_cast_signals()

#thread1 = threading.Thread(target = send_random_vote_cast_signals)
# set daemon = 'True' so thread will die when test server is shut down
#thread1.daemon = 'True'
#thread1.start()

