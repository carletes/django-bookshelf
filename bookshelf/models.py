from __future__ import unicode_literals

import logging
import mimetypes
import os

from collections import defaultdict

from django.db import models

from ebooklib import epub

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


def pdf_metadata(fname):
    ret = {}
    with open(fname, "rb") as f:
        p = pdfparser.PDFParser(f)
        doc = pdfdocument.PDFDocument(p)

        for info in doc.info:
            for k in info:
                try:
                    v = info[k].resolve()
                except AttributeError:
                    v = str(info[k])
                ret[k.lower()] = v
    return ret


def epub_metadata(fname):
    ret = {}
    try:
        book = epub.read_epub(fname)
        for values in book.metadata.values():
            for k in values:
                if k == "creator":
                    field = "author"
                else:
                    field = k
                ret[field] = values[k][0][0]
    except:
        pass
    return ret


mimetypes.add_type("application/epub+zip", ".epub")


METADATA_READERS = defaultdict(lambda: {}, {
    "application/epub+zip": epub_metadata,
    "application/pdf": pdf_metadata,
})

FORMATS = {
    "application/epub+zip": "ePub",
    "application/pdf": "PDF",
}


class Document(models.Model):

    path = models.FileField(upload_to=document_path)

    @property
    def metadata(self):
        if not hasattr(self, "_metadata"):
            self._metadata = METADATA_READERS[self.mimetype](self.path.path)
        return self._metadata

    @property
    def format(self):
        return FORMATS.get(self.mimetype, "<Unknown>")

    @property
    def mimetype(self):
        return mimetypes.guess_type(self.path.path, strict=False)[0]

    def __unicode__(self):
        return os.path.basename(self.path.path)


class Title(models.Model):

    authors = models.ManyToManyField(Author)
    title = models.CharField(max_length=512)
    documents = models.ManyToManyField(Document)

    class Meta:

        ordering = ['title']

    def __unicode__(self):
        return self.title
