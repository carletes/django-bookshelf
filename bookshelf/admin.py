import logging

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from . import models


class AuthorAdmin(admin.ModelAdmin):

    pass


class DocumentAdmin(admin.ModelAdmin):

    pass


class TitleAdmin(admin.ModelAdmin):

    actions = ["merge_titles"]
    filter_horizontal = ["authors", "documents"]
    list_display = ["title", "author_names", "formats"]

    log = logging.getLogger(__name__)

    def author_names(self, title):
        return ",".join(author.name for author in title.authors.all())

    def formats(self, title):
        return ", ".join(doc.format for doc in title.documents.all())

    author_names.short_description = "Authors"

    def merge_titles(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        titles = ",".join(selected)
        return HttpResponseRedirect(reverse("bookshelf:merge-titles") +
                                    ("?titles=%s" % (titles,)))

    merge_titles.short_description = "Merge selected titles"


admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Document, DocumentAdmin)
admin.site.register(models.Title, TitleAdmin)
