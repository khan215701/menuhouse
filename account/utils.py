from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from menuhouse.settings import DEFAULT_FROM_EMAIL

def detectUser(user):
    if user.role == 1:
        redirecturl = 'vendorDashboard'
        return redirecturl
    elif user.role == 2:
        redirecturl = 'customerDashboard'
        return redirecturl
    elif user.role == None and user.is_superadmin:
        redirecturl = '/admin'
        return redirecturl
    
    
def send_email(request,user, subject, template):
    from_email = DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    mail_subject = subject
    message = render_to_string(template,{
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()
    
    
def send_notification(mail_subject, template, context):
    from_email = DEFAULT_FROM_EMAIL
    message = render_to_string(template, context)
    to_email = context['user'].email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()

    
