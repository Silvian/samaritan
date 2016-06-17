"""
@author: Silvian Dragan
@Date: 17/06/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def send_group_emails(from_email, recipient_name, subject):
    text_template = get_template('samaritan/email/group_email.txt')
    html_template = get_template('samaritan/email/group_email.html')

    context = {'username': recipient_name}
    text_content = text_template.render(context)
    html_content = html_template.render(context)

    to = ['email@example.com']

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    return msg.send()


