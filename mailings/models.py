from django.db import models
from users.models import User

NULLABLE = {'blank': True, 'null': True}
NOTNULLABLE = {'blank': False, 'null': False}


class Client(models.Model):
    """Клиенты получатели рассылок"""
    objects = None
    first_name = models.CharField(max_length=150, verbose_name='Фамилия', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='Имя', **NULLABLE)
    email = models.EmailField(verbose_name='Почта', unique=True)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Владелец')

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        permissions = [
            ("set_is_block", "Can block client"),
            ("view_clients_list", "Can view clients list"),
        ]


class Message(models.Model):
    objects = None
    subject_line = models.CharField(max_length=50, verbose_name="Тема", **NOTNULLABLE, unique=True)
    body = models.TextField(max_length=500, verbose_name="Сообщение", **NOTNULLABLE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Владелец')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.subject_line}'


class Mailing(models.Model):
    """Рассылка"""
    STATUS = (
        ('start', 'start'),
        ('finish', 'finish'),
        ('created', 'created')
    )
    PERIOD = (
        ("daily", "daily"),
        ("weekly", "weekly"),
        ("monthly", "monthly"),
    )
    objects = None
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    date_time_first_send = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время первой отправки')
    period = models.CharField(max_length=20, choices=PERIOD, verbose_name='Период рассылки')
    status = models.CharField(max_length=20, choices=STATUS, default='created', verbose_name='Статус')
    clients = models.ManyToManyField(Client, verbose_name='Получатели')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Отправитель')

    def __str__(self):
        return f'{self.message}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ("set_is_deactivate", "Can deactivate mailing"),
            ("view_all_mailings", "Can view all mailings"),
        ]


class MailingStatistic(models.Model):
    """ Cтатистика рассылок"""
    STATUS_MAILING = (
        ('success', 'success'),
        ('failure', 'failure'),
    )
    objects = None
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    date_time_last_attempt = models.DateTimeField(auto_now=True, verbose_name='Дата и время последней попытки')
    status_attempt = models.CharField(max_length=20, choices=STATUS_MAILING, verbose_name='Статус попытки')
    response = models.TextField(**NULLABLE, verbose_name='Ответ сервера')

    def __str__(self):
        return f"{self.mailing}"

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'
