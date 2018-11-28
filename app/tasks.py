from app import celery
from flask_mail import Message
from app import mail


@celery.task(name='celery_add_together')
def add_together():
    # t.sleep(10)
    print('YOU ARE HERE NOW')
    return 'OK'


@celery.task(name='send_pkg_notification')
def send_pkg_notif(recipient):
    # recipient = 'krsteski_aleksandar@hotmail.com'

    msg = Message('Ova e proba', recipients=[recipient])
    msg.body = 'Proba'
    msg.html = '<b>Html Proba</b>'
    mail.send(msg)

    return 'Send notification mail to: %s' % recipient

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls add together every 10 seconds.
    sender.add_periodic_task(
        10.0, add_together, name='add together 10 seconds')

    # # Call send_pkg_notif every 30 seconds.
    # sender.add_periodic_task(
    #     30.0, send_pkg_notif, name='send pkg notif 30 seconds',
    #     args=['krsteski_aleksandar@hotmail.com'])
