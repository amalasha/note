from django import forms
from notes_app.models import Note, Tag


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('note', 'tags',)


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('tag',)