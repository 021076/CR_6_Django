from datetime import datetime
import pytz
from django.core.mail import send_mail

from config import settings
from mailings.models import Mailing, MailingStatistic


def mail_sending(subject_line, body, owner, adressee_list):
    send_mail(
        subject_line,
        body,
        owner,
        [adressee_list]
    )


def period_mail_sending():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Mailing.objects.filter(date_time_first_sand__lte=current_datetime).filter(
        status__in=['created', 'start'])
    try:
        for mailing in mailings:
            if mailing.period == 'daily':
                if mailing.date_time_first_sand.hour == current_datetime.hour and mailing.date_time_first_sand.minute == current_datetime.minute:
                    mail_sending(mailing.message.subject_line, mailing.message.body, mailing.owner, mailing.clients)
            elif mailing.period == 'weekly':
                if ((
                            mailing.date_time_first_sand - current_datetime).days % 7 == 0) and mailing.date_time_first_sand.hour == current_datetime.hour and \
                        mailing.date_time_first_sand.minute == current_datetime.minute:
                    mail_sending(mailing.message.subject_line, mailing.message.body, mailing.owner, mailing.clients)
            elif mailing.period == 'monthly':
                if ((
                            mailing.date_time_first_sand - current_datetime).days % 31 == 0) and mailing.date_time_first_sand.hour == current_datetime.hour and \
                        mailing.date_time_first_sand.minute == current_datetime.minute:
                    mail_sending(mailing.message.subject_line, mailing.message.body, mailing.owner, mailing.clients)
        statistic = MailingStatistic(mailing=mailing, date_time_last_attempt=current_datetime,
                                     status_attempt='success', response='success')
        statistic.save()
    except Exception:
        statistic = MailingStatistic(mailing=mailing, date_time_last_attempt=current_datetime,
                                     status_attempt='failure', response='failure')
        statistic.save()
    mailing.save()
