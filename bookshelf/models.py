from __future__ import unicode_literals

import logging
import os

from django.db import models


__all__ = [
    "Author",
    "Document",
    "Title",
]


LOG = logging.getLogger(__name__)


class Author(models.Model):

    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name


def document_path(instance, filename):
    return os.path.basename(instance.path.path)


class Document(models.Model):

    format = models.CharField(max_length=32)
    path = models.FileField(upload_to=document_path)

    def __unicode__(self):
        return os.path.basename(self.path.path)


class Title(models.Model):

    authors = models.ManyToManyField(Author)
    title = models.CharField(max_length=512)
    documents = models.ManyToManyField(Document)

    def __unicode__(self):
        return self.title
