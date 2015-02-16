# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InvitationKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=40, verbose_name='invitation key')),
                ('email', models.EmailField(max_length=75)),
                ('date_invited', models.DateTimeField(default=datetime.datetime.now, verbose_name='date invited')),
                ('from_user', models.ForeignKey(related_name='invitations_sent', to=settings.AUTH_USER_MODEL)),
                ('registrant', models.ForeignKey(related_name='invitations_used', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InvitationUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invitations_remaining', models.IntegerField()),
                ('inviter', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
