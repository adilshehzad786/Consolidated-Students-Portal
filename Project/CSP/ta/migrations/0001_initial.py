# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Students', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='TA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=100)),
                ('coursecode', models.ForeignKey(to='portal.Course')),
                ('rollno', models.ForeignKey(to='Students.Student', to_field=b'rollno')),
                ('username', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field=b'email')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
