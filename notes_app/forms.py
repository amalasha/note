from django import forms
from notes_app.models import Note, Tag


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        widgets = {
            'note': forms.Textarea(attrs={'rows':'6','class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        fields = ('note', 'tags',)


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('tag',)