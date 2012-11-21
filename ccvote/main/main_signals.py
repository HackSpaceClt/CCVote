from django.dispatch import Signal

vote_open_signal = Signal()
vote_cast_signal = Signal(providing_args=['motion_id', 'user_id', 'vote'])
