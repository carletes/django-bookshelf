from django import forms

from .models import Author, Document, Title


__all__ = [
    "MergeForm",
]


class MergeForm(forms.Form):

    title = forms.ModelChoiceField(label="Title", queryset=None)
    authors = forms.ModelMultipleChoiceField(label="Authors", queryset=None)
    documents = forms.ModelMultipleChoiceField(label="Document", queryset=None)
    from_title_ids = forms.MultipleChoiceField(widget=forms.MultipleHiddenInput())

    def __init__(self, *args, **kwargs):
        super(MergeForm, self).__init__(*args, **kwargs)
        from_title_ids = kwargs.get("from_title_ids", [])
        self.fields["title"].queryset = Title.objects.filter(pk__in=from_title_ids)
        self.fields["authors"].queryset = Author.objects.filter(titles__in=kwargs.get("author_ids", []))
        self.fields["documents"].queryset = Document.objects.filter(pk__in=kwargs.get("document_ids", []))
