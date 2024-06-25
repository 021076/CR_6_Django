from apscheduler.schedulers.background import BackgroundScheduler
from mailings.options import period_mail_sending


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(period_mail_sending, "interval", minutes=1)
    scheduler.start()
    print('Планировщик запущен')
