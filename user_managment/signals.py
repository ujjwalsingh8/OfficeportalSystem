from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_init, pre_save, pre_delete, post_init, post_save
from user_managment.hepler import send_email_on_login


@receiver(user_logged_in, sender = User)
def login_success(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    request.session['ip'] = ip
    send_email_on_login(request, ip)

# @receiver(pre_init, sender = User)
# def logout_success(sender, *args, **kwargs):
#     print('-------------logout--------')
#     print('sender',sender)
#     # print('request',request)
#     # print('user', user)
#     print(f'kwargs,{kwargs}')


# @receiver(post_init, sender = User)
# def logut_success(sender, *args, **kwargs):
#     print('-------------logo     ut--------')
#     print('sender',sender)
#     # print('request',request)
#     # print('user', user)
#     print(f'kwargs,{kwargs}')

# @receiver(user_login_failed)
# def login_failed(sender, request, credentials, **kwargs):
#     print('-------------login failed--------')
#     print('sender',sender)
#     print('request',request)
#     print('credentials', credentials)
#     print(f'kwargs,{kwargs}')

# @receiver(pre_save, sender = User)
# def at_beginning_save(sender, instance, **kwargs):
#     print('------------------')
#     print('sender',sender)
#     print('request',instance)
#     print(f'kwargs,{kwargs}')
