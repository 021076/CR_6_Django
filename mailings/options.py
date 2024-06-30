from datetime import datetime
import pytz
from django.core.mail import send_mail
from config import settings
from mailings.admin import MailingAdmin
from mailings.models import Mailing, MailingStatistic


def mail_sending(subject, message, from_email, recipient_list):
    send_mail(
        subject,
        message,
        from_email,
        [recipient_list]
    )


def period_mail_sending():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Mailing.objects.filter(status__in=['created', 'start'])
    print(mailings)
    try:
        for mailing in mailings:
            if mailing.period == 'daily' and mailing.date_time_first_send.hour == current_datetime.hour and mailing.date_time_first_send.minute == current_datetime.minute:
                    mail_sending(mailing.message.subject_line, mailing.message.body, mailing.owner, mailing.clients)
            elif mailing.period == 'weekly' and ((
                            mailing.date_time_first_send - current_datetime).days % 7 == 0) and mailing.date_time_first_send.hour == current_datetime.hour and \
                        mailing.date_time_first_send.minute == current_datetime.minute:
                    mail_sending(mailing.message.subject_line, mailing.message.body, mailing.owner, mailing.clients)
            elif mailing.period == 'monthly'and ((
                            mailing.date_time_first_send - current_datetime).days % 31 == 0) and mailing.date_time_first_send.hour == current_datetime.hour and \
                        mailing.date_time_first_send.minute == current_datetime.minute:
                    mail_sending(mailing.message.subject_line, mailing.message.body, mailing.owner, mailing.clients)
            statistic = MailingStatistic(mailing=mailing, date_time_last_attempt=current_datetime,
                                     status_attempt='success', response='success')
            statistic.save()
    except Exception:
        statistic = MailingStatistic(mailing=mailing, date_time_last_attempt=current_datetime,
                                     status_attempt='failure', response='failure')
        statistic.save()
    mailing.save()
