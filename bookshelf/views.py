from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .models import Document, Title


__all__ = [
    "TitleList",
    "DocumentCreate",
]


class DocumentCreate(CreateView):

    model = Document
    fields = ["path"]
    success_url = reverse_lazy("bookshelf:index")

    def form_valid(self, form):
        response = super(DocumentCreate, self).form_valid(form)
        metadata = form.instance.metadata
        if "Title" in metadata:
            title = Title(title=metadata["Title"])
            authors = metadata.get("Author", "").split(",")
            for author in authors:
                pass
            title.save()
        return response


class TitleList(ListView):

    model = Title
