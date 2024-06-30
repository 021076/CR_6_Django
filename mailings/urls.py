from apscheduler.schedulers.background import BackgroundScheduler
from django.urls import path
from mailings.apps import MailingsConfig
from mailings.options import period_mail_sending
from mailings.views import MailingListView, MailingCreateView, MailingDetailView, MailingUpdateView, MailingDeleteView, \
    ClientListView, ClientCreateView, ClientUpdateView, ClientDetailView, ClientDeleteView, MailingStatisticListView, \
    MessageListView, MessageCreateView, MessageUpdateView, MessageDetailView, MessageDeleteView, \
    MailingStatisticDetailView

app_name = MailingsConfig.name

urlpatterns = [
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/detail/', ClientDetailView.as_view(), name='client_detail'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/detail/', MessageDetailView.as_view(), name='message_detail'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/<int:pk>/detail/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailingstatistic/', MailingStatisticListView.as_view(), name='mailingstatistic_list'),
    path('mailingstatistic/<int:pk>/detail/', MailingStatisticDetailView.as_view(), name='mailingstatistic_detail'),
   ]
