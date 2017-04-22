# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-21 20:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import easy_thumbnails.fields
import userena.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mugshot', easy_thumbnails.fields.ThumbnailerImageField(blank=True, help_text='A personal image displayed in your profile.', upload_to=userena.models.upload_to_mugshot, verbose_name='mugshot')),
                ('privacy', models.CharField(choices=[('open', 'Open'), ('registered', 'Registered'), ('closed', 'Closed')], default='registered', help_text='Designates who can view your profile.', max_length=15, verbose_name='privacy')),
                ('location', models.CharField(blank=True, max_length=30)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_profile', 'Can view profile'),),
                'abstract': False,
            },
        ),
    ]
