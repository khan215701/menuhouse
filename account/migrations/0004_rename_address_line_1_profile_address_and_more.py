# Generated by Django 4.1.3 on 2022-11-29 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_user_role'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='address_line_1',
            new_name='address',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='address_line_2',
        ),
    ]
