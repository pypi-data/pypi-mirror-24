# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-03 13:48
from __future__ import unicode_literals

import crate_anon.crateweb.consent.models
import crate_anon.crateweb.consent.storage
import crate_anon.crateweb.extra.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consent', '0004_auto_20160703_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailattachment',
            name='file',
            field=models.FileField(storage=crate_anon.crateweb.consent.storage.CustomFileSystemStorage(base_url='download_privatestorage', location='C:/srv/crate_filestorage'), upload_to=''),  # noqa
        ),
        migrations.AlterField(
            model_name='leaflet',
            name='pdf',
            field=crate_anon.crateweb.extra.fields.ContentTypeRestrictedFileField(blank=True, storage=crate_anon.crateweb.consent.storage.CustomFileSystemStorage(base_url='download_privatestorage', location='C:/srv/crate_filestorage'), upload_to=crate_anon.crateweb.consent.models.leaflet_upload_to),  # noqa
        ),
        migrations.AlterField(
            model_name='letter',
            name='pdf',
            field=models.FileField(storage=crate_anon.crateweb.consent.storage.CustomFileSystemStorage(base_url='download_privatestorage', location='C:/srv/crate_filestorage'), upload_to=''),  # noqa
        ),
        migrations.AlterField(
            model_name='study',
            name='study_details_pdf',
            field=crate_anon.crateweb.extra.fields.ContentTypeRestrictedFileField(blank=True, storage=crate_anon.crateweb.consent.storage.CustomFileSystemStorage(base_url='download_privatestorage', location='C:/srv/crate_filestorage'), upload_to=crate_anon.crateweb.consent.models.study_details_upload_to),  # noqa
        ),
        migrations.AlterField(
            model_name='study',
            name='subject_form_template_pdf',
            field=crate_anon.crateweb.extra.fields.ContentTypeRestrictedFileField(blank=True, storage=crate_anon.crateweb.consent.storage.CustomFileSystemStorage(base_url='download_privatestorage', location='C:/srv/crate_filestorage'), upload_to=crate_anon.crateweb.consent.models.study_form_upload_to),  # noqa
        ),
    ]
