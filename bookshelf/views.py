import logging

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .models import Author, Document, Title
from .forms import MergeForm


__all__ = [
    "TitleList",
    "DocumentCreate",
    "merge_titles",
]


LOG = logging.getLogger(__name__)


class DocumentCreate(CreateView):

    model = Document
    fields = ["path"]
    success_url = reverse_lazy("bookshelf:index")

    def form_valid(self, form):
        response = super(DocumentCreate, self).form_valid(form)
        document = form.instance
        metadata = document.metadata
        if "title" in metadata:
            title, created = Title.objects.get_or_create(title=metadata["title"])
            if created:
                authors = metadata.get("author", "").split(",")
                for name in authors:
                    author, _ = Author.objects.get_or_create(name=name)
                    title.authors.add(author)

            documents = [document]
            for d in title.documents.all():
                if d.mimetype != document.mimetype:
                    documents.append(d)
            title.documents.set(documents, clear=True)
            title.save()
        return response


class TitleList(ListView):

    model = Title


def merge_titles(request):
    titles_index = reverse("admin:bookshelf_title_changelist")

    title_ids = []
    author_ids = []
    document_ids = []
    for title_id in request.GET.get("titles", "").split(","):
        try:
            title = Title.objects.get(pk=title_id)
            title_ids.append(title.pk)
            author_ids.extend(a.pk for a in title.authors.all())
            document_ids.extent(d.pk for d in title.documents.all())
        except Title.DoesNotExist:
            pass

    if request.method == "POST":
        form_params = dict(request.POST)
        form_params.
        form = MergeForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(titles_index)

    if len(title_ids) < 2:
        return HttpResponseRedirect(titles_index)


    params = {
        "title_ids": title_ids,
        "author_ids": author_ids,
        "document_ids": document_ids,
        "form
    }
    return render(request, "bookshelf/merge_titles.html", params)
