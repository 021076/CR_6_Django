from django.contrib import admin
from mailings.models import Client, Mailing, MailingStatistic, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'comment', 'owner',)
    search_fields = ('email', 'first_name', 'owner',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject_line', 'body', 'owner',)
    search_fields = ('subject_line', 'owner',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('message', 'date_time_first_send', 'period', 'status', 'owner', 'client_list')
    search_fields = ('subject_line', 'period', 'status', 'owner',)

    def client_list(self, obj):
        client_list = []
        for client in obj.clients.all():
            client_list.append(client.email)
        return ', '.join(client_list)


@admin.register(MailingStatistic)
class MailingStatisticAdmin(admin.ModelAdmin):
    list_display = ('date_time_last_attempt', 'status_attempt', 'mailing', 'response')
    search_fields = ('status_attempt', 'response', 'mailing',)
