# Generated by Django 2.1.4 on 2019-01-28 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_userbooks_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userbooks',
            old_name='user',
            new_name='user_id',
        ),
    ]