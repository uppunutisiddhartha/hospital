# utils.py (or inside views.py)

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .models import *

def send_post_newsletter(post):
    subscribers = newsletter_subscribers.objects.values_list('email', flat=True)

    if not subscribers:
        return

    html_content = render_to_string(
        'email_templates/new_post_newsletter.html',
        {'post': post}
    )

    email = EmailMessage(
        subject=f"New Update: {post.title}",
        body=html_content,
        from_email=settings.EMAIL_HOST_USER,
        bcc=list(subscribers),
    )
    email.content_subtype = "html"
    email.send(fail_silently=True)



#specific login required decorator
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
