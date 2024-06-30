# Generated by Django 4.2 on 2024-06-30 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0003_alter_mailing_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'permissions': [('set_is_block', 'Can block client'), ('view_clients_list', 'Can view clients list')], 'verbose_name': 'Клиент', 'verbose_name_plural': 'Клиенты'},
        ),
        migrations.AlterModelOptions(
            name='mailing',
            options={'permissions': [('set_is_deactivate', 'Can deactivate mailing'), ('view_all_mailings', 'Can view all mailings')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
    ]