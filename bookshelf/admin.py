from django.contrib import admin

from . import models


class AuthorAdmin(admin.ModelAdmin):

    pass


class DocumentAdmin(admin.ModelAdmin):

    pass


class TitleAdmin(admin.ModelAdmin):

    pass


admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Document, DocumentAdmin)
admin.site.register(models.Title, TitleAdmin)
