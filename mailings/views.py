from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from mailings.forms import ClientForm, MailingForm, MessageForm
from mailings.models import Client, Mailing, MailingStatistic, Message


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm

    def form_valid(self, form):
        if form.is_valid():
            edit_client = form.save()
            edit_client.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailings:client_detail', args=[self.kwargs.get('pk')])

    def test_func(self):
        user = self.request.user
        client = self.get_object()
        if client.owner == user or user.is_superuser:
            return True
        return False


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:client_list')

    def test_func(self):
        user = self.request.user
        client = self.get_object()
        if client.owner == user or user.is_superuser:
            return True
        return False


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailings/client_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        client_list = Client.objects.all()
        context['client_list'] = client_list
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(owner=self.request.user)
        return queryset


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailings/client_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.get_object()
        context['client'] = client
        return context


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    form_class = MessageForm

    def form_valid(self, form):
        if form.is_valid():
            edit_message = form.save()
            edit_message.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailings:message_detail', args=[self.kwargs.get('pk')])

    def test_func(self):
        user = self.request.user
        message = self.get_object()
        if message.owner == user or user.is_superuser:
            return True
        return False


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailings:message_list')

    def test_func(self):
        user = self.request.user
        message = self.get_object()
        if message.owner == user or user.is_superuser:
            return True
        return False


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailings/message_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        message_list = Message.objects.all()
        context['message_list'] = message_list
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(owner=self.request.user)
        return queryset


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailings/message_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message = self.get_object()
        context['message'] = message
        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailing_list')

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingForm

    def form_valid(self, form):
        if form.is_valid():
            edit_mailing = form.save()
            edit_mailing.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailings:mailing_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user == self.request.user.is_staff:
            return MailingForm
        raise PermissionDenied

    def test_func(self):
        user = self.request.user
        mailing = self.get_object()
        if mailing.owner == user or user.is_superuser:
            return True
        return False


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailings:mailing_list')

    def test_func(self):
        user = self.request.user
        mailing = self.get_object()
        if mailing.owner == user or user.is_superuser:
            return True
        return False


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        mailings_list = Mailing.objects.all()
        context['mailings_list'] = mailings_list
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing = self.get_object()
        context['mailing'] = mailing
        return context


class MailingStatisticListView(ListView):
    model = MailingStatistic
    template_name = 'mailings/mailingstatistic_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        mailingstatistic_list = MailingStatistic.objects.all()
        context['mailingstatistic_list'] = mailingstatistic_list
        return context


class MailingStatisticDetailView(DetailView):
    model = MailingStatistic
    template_name = 'mailings/mailingstatistic_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailingstatistic = self.get_object()
        context['mailingstatistic'] = mailingstatistic
        return context
