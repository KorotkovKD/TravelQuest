from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .tokens import account_activation_token

MAIL_SUBJECT_ACTIVASION = 'Activate your user account.'
#MAIL_MESSAGE_ACTIVASION = ''

def create_activation_link(request, user):
    domain = get_current_site(request).domain
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    if request.is_secure():
        protocol = 'https://'
    else:
        protocol = 'http://'
    return protocol+domain+'/'+uid+'/'+token
