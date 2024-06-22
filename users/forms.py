from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User


class UserRegisertForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
