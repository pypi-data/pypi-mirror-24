# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-07 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consent', '0007_auto_20170228_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consentmode',
            name='consent_mode',
            field=models.CharField(choices=[('red', 'red'), ('yellow', 'yellow'), ('green', 'green')], default='', max_length=10, verbose_name='Consent mode (red/yellow/green)'),  # noqa
        ),
        migrations.AlterField(
            model_name='consentmode',
            name='source',
            field=models.CharField(default='crate_user_entry', max_length=20, verbose_name='Source of information'),  # noqa
        ),
        migrations.AlterField(
            model_name='leaflet',
            name='name',
            field=models.CharField(choices=[('cpft_tpir', 'CPFT: Taking part in research [MANDATORY]'), ('nihr_yhrsl', 'NIHR: Your health records save lives [not currently used]'), ('cpft_trafficlight_choice', 'CPFT: traffic-light choice decision form [not currently used: personalized version created instead]'), ('cpft_clinres', 'CPFT: clinical research [not currently used]')], max_length=50, unique=True, verbose_name='leaflet name'),  # noqa
        ),
    ]
