# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PushedData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('doi', models.TextField()),
                ('tags', models.TextField()),
                ('title', models.TextField()),
                ('serviceID', models.TextField()),
                ('description', models.TextField()),
                ('contributors', models.TextField()),
                ('dateUpdated', models.DateField(auto_now_add=True)),
                ('source', models.ForeignKey(related_name='data', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
