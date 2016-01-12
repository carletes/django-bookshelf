# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-12 14:04
from __future__ import unicode_literals

import bookshelf.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('format', models.CharField(max_length=32)),
                ('path', models.FileField(upload_to=bookshelf.models.document_path)),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('authors', models.ManyToManyField(to='bookshelf.Author')),
                ('documents', models.ManyToManyField(to='bookshelf.Document')),
            ],
        ),
    ]