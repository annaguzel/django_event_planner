# Generated by Django 2.2.5 on 2020-03-03 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_auto_20200303_1932'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='following',
        ),
    ]