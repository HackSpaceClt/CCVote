from django.dispatch import Signal

vote_open_signal = Signal(providing_args=['motion_id'])
vote_close_signal = Signal(providing_args=['motion_id'])
vote_cast_signal = Signal(providing_args=['motion_id', 'user_id', 'vote'])
