from django.shortcuts import render
from django.views.generic import ListView
from notes_app.models import Note, Tag
from django.template import RequestContext
from notes_app.forms import NoteForm, TagForm
import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse


def tag(request):
    return render(request, 'notes_app/tag.html')


# for notes page
class NotesListView(ListView):
    model = Note
    paginate_by = 10
    template_name = 'notes_app/list.html'


def note_action(request, pk=None):
    print(pk)
    if request.method == "POST":
        print(request.POST)
        if pk is None:
            form = NoteForm(request.POST)
        else:
            notes = get_object_or_404(Note, pk=pk)
            form = NoteForm(request.POST, instance=notes)
        if form.is_valid():
            form.save()
            return HttpResponsePermanentRedirect(reverse('notes_app:home'))
    else:
        if pk is not None:
            notes = get_object_or_404(Note, pk=pk)
            form = NoteForm(instance=notes)
        else:
            form = NoteForm()
        return render(request, 'notes_app/add_note.html', {'form': form})


def delete_note(request, pk):
    notes = get_object_or_404(Note, pk=pk)
    notes.delete()
    return HttpResponsePermanentRedirect(reverse('notes_app:home'))


