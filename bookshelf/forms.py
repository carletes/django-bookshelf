from django import forms

from .models import Author, Document, Title


__all__ = [
    "MergeForm",
]


class MergeForm(forms.Form):

    title = forms.ModelChoiceField(label="Title", queryset=None)
    authors = forms.ModelMultipleChoiceField(label="Authors", queryset=None)
    documents = forms.ModelMultipleChoiceField(label="Document", queryset=None)
    from_titles = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(MergeForm, self).__init__(*args, **kwargs)
        from_titles = kwargs.get("initial", self.data).get("from_titles")
        if from_titles:
            from_titles = from_titles.split(",")
            self.fields["title"].queryset = Title.objects.filter(pk__in=from_titles).distinct()
            self.fields["authors"].queryset = Author.objects.filter(title__pk__in=from_titles).distinct()
            self.fields["documents"].queryset = Document.objects.filter(title__pk__in=from_titles).distinct()
