# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-11 09:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warrenty', '0003_auto_20171111_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerwarrenty',
            name='warranty_expire_date',
            field=models.DateField(editable=False, verbose_name='Expire Date'),
        ),
    ]
