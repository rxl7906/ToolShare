# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '__first__'),
        ('users', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('tool_name', models.CharField(max_length=50)),
                ('tool_type', models.CharField(max_length=50)),
                ('tool_availability', models.CharField(max_length=50)),
                ('borrower', models.ForeignKey(related_name='+', to='users.User', default=None, to_field='username', null=True)),
                ('owner', models.ForeignKey(to_field='username', to='users.User', related_name='+')),
                ('zip_code', models.ForeignKey(to_field='zip_code', to='communities.Community', related_name='+')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
