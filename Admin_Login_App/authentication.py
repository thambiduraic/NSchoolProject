from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from knox.auth import AuthToken
import sys


#this return left time
def expires_in(token):
    print(type(token))
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    return left_time

# token checker if token expired or not
def is_token_expired(token):
    return expires_in(token) < timedelta(seconds = 0)

# if token is expired new token will be established
# If token is expired then it will be removed
# and new one with different key will be created
def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = AuthToken.objects.create(user = token.user)
    return is_expired, token
