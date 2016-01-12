from __future__ import unicode_literals

import logging
import os

from django.db import models

from pdfminer import pdfparser, pdfdocument


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

    path = models.FileField(upload_to=document_path)

    @property
    def metadata(self):
        if not hasattr(self, "_metadata"):
            with open(self.path.path, "rb") as f:
                self._metadata = {}
                p = pdfparser.PDFParser(f)
                doc = pdfdocument.PDFDocument(p)

                for info in doc.info:
                    for k in info:
                        try:
                            v = info[k].resolve()
                        except AttributeError:
                            v = str(info[k])
                        self._metadata[k] = v
        return self._metadata

    def __unicode__(self):
        return os.path.basename(self.path.path)


class Title(models.Model):

    authors = models.ManyToManyField(Author)
    title = models.CharField(max_length=512)
    documents = models.ManyToManyField(Document)

    def __unicode__(self):
        return self.title
