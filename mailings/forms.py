from django import forms
from django.forms import ModelForm, BooleanField
from mailings.models import Client, Mailing, MailingStatistic, Message


class StyleMixin(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        # ('first_name', 'last_name', 'email', 'comment')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MessageForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
        # ('subject_line', 'body',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'
        # ('message', 'period', 'status', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        # self.fields["message"].widget.attrs['class'] = 'select'
        # self.fields["client"].widget.attrs['class'] = 'select'
        self.fields["period"].widget.attrs['class'] = 'select'
        self.fields["status"].widget.attrs['class'] = 'select'


class MailingStatisticForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = MailingStatistic
        fields = '__all__'
        # ('status_attempt', 'mailing', 'response',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
