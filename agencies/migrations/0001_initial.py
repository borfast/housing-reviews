# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('logo', models.ImageField(height_field=b'logo_height', width_field=b'logo_width', null=True, upload_to=b'agencies_logos', blank=True)),
                ('logo_width', models.PositiveIntegerField(null=True, blank=True)),
                ('logo_height', models.PositiveIntegerField(null=True, blank=True)),
                ('website', models.CharField(max_length=100, null=True, blank=True)),
                ('rating_votes', models.PositiveIntegerField(default=0, editable=False, blank=True)),
                ('rating_score', models.IntegerField(default=0, editable=False, blank=True)),
            ],
            options={
                'verbose_name_plural': 'agencies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField(null=True, blank=True)),
                ('post_code', models.CharField(max_length=100, null=True, blank=True)),
                ('agency', models.ForeignKey(to='agencies.Agency')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='agency',
            name='main_office',
            field=models.ForeignKey(related_name='main_office', blank=True, to='agencies.Office', null=True),
            preserve_default=True,
        ),
    ]
