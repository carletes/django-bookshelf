import logging

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext
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

    if request.method == "POST":
        from_titles = request.POST.get("from_titles", "")
        form = MergeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            from_titles = data["from_titles"].split(",")
            for t in Title.objects.filter(pk__in=from_titles):
                if t == data["title"]:
                    t.authors.set(data["authors"], clear=True)
                    t.documents.set(data["documents"], clear=True)
                    t.save()
                else:
                    t.delete()
            return HttpResponseRedirect(titles_index)
    else:
        from_titles = request.GET.get("from_titles")
        form = MergeForm(initial={"from_titles": from_titles})

    return render(request, "bookshelf/merge_titles.html",
                  {
                      "form": form,
                      "has_permission": True,
                      "title": ugettext("Merge titles"),
                  })
