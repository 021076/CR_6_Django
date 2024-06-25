import random
import secrets
import string

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisertForm, UserEditForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisertForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        # user.verified = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/verification/{token}/'
        send_mail('Подтверждение почты',
                  f'Перейдите по ссылке для подтверждения почты {url}',
                  EMAIL_HOST_USER,
                  [user.email]
                  )
        print(url)
        return super().form_valid(form)


def verification(request, token):
    user = get_object_or_404(User, token=token)
    # user.verified = True
    user.is_active = True
    user.save(update_fields=['is_active'])
    return redirect(reverse('users:login'))


class EditView(UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('main:index')

    def get_object(self, queryset=None):
        return self.request.user


def password_reset(request):
    """Сбрасывает пароль пользователя"""
    context = {'success_message': 'Пароль успешно сброшен. Новый пароль был отправлен на ваш адрес электронной почты.'}
    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_object_or_404(User, email=email)
        characters = string.ascii_letters + string.digits
        characters_list = list(characters)
        random.shuffle(characters_list)
        password = ''.join(characters_list[:10])
        user.set_password(password)
        user.save()
        send_mail(
            subject='Восстановление пароля',
            message=f'Вы получили это электронное письмо, потому что запросили восстановление пароля'
                    f' для своей учетной записи "{user}". Ваш новый пароль: {password}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return render(request, 'users/password_reset.html', context)
    else:
        return render(request, 'users/password_reset.html')
