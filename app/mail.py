
from django.conf import settings
from django.template import Context, loader
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver




def send_contact_mail():
    if True:
        subject = "Thank you for registering with us"
        to = 'nwabuezedavid666@gmail.com'
        val =  { 
                'subject':subject,
                }

        html_content = render_to_string('mail/alert.html',val)
        text_content = strip_tags(html_content)
        from_email = settings.DEFAULT_FROM_EMAIL
        msg_html = render_to_string('mails/registration.html',val)
        send_mail(subject, None, from_email,to,html_message=msg_html)

send_contact_mail()

