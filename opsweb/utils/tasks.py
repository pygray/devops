from __future__ import absolute_import, unicode_literals
from .mail import Mail
from celery import shared_task

@shared_task(name="send_mail")
def send_mail(to_list, personnel, sqlid, note, action_type, sqlcontent, dbname):
    return Mail.send(to_list, personnel, sqlid, note, action_type, sqlcontent, dbname)