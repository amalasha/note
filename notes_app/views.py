from django.shortcuts import render
from django.views.generic import ListView
from notes_app.models import Note, Tag
from django.template import RequestContext
from notes_app.forms import NoteForm, TagForm
import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json


class TagsListView(ListView):
    """
    Lists the tags
    """
    model = Tag
    paginate_by = 10
    template_name = 'notes_app/tag.html'


def tag_action(request, pk=None):
    """
        Tag add / edit
    """
    if request.method == "POST":
        print(request.POST)
        if pk is None:
            form = TagForm(request.POST)
        else:
            tags = get_object_or_404(Tag, pk=pk)
            form = TagForm(request.POST, instance=tags)
        if form.is_valid():
            form.save()
            return HttpResponsePermanentRedirect(reverse('notes_app:tag'))
    else:
        if pk is not None:
            tags = get_object_or_404(Tag, pk=pk)
            form = TagForm(instance=tags)
        else:
            form = TagForm()
        return render(request, 'notes_app/add_tag.html', {'form': form})


def addtag(request):
    """
    tag addition
    """
    if request.method == 'POST':
        tag = request.POST["tag"]
        t = Tag.objects.create(tag=tag)
        response_data = {}
        response_data['id'] = t.pk
        response_data['tag'] = t.tag
        return HttpResponse(json.dumps(response_data), content_type="application/json")


# for tag delete
def delete_tag(request, pk):
    """
    tag deletion
    """
    tags = get_object_or_404(Tag, pk=pk)
    tags.delete()
    return HttpResponsePermanentRedirect(reverse('notes_app:tag'))


def home(request, id = '0'):
    if id is None or id == '0':
        notes_list = Note.objects.all()
    else:
        notes_list = Note.objects.filter(tags__id=id)
    tag_list = Tag.objects.all()
    paginator = Paginator(notes_list, 10)  # Show 25 contacts per page

    page = request.GET.get('page')

    try:

        notes = paginator.page(page)

    except PageNotAnInteger:

        # If page is not an integer, deliver first page.

        notes = paginator.page(1)

    except EmptyPage:

        # If page is out of range (e.g. 9999), deliver last page of results.

        notes = paginator.page(paginator.num_pages)

    return render(request, 'notes_app/list.html', {'note': notes, 'tag': tag_list, 'selected_id': int(id)})


# for index page
class IndexView(ListView):
    paginate_by = 10
    template_name = 'notes_app/list.html'
    context_object_name = "note_list"
    queryset = Note.objects.all().order_by('-created_date')

    def get_context_data(self, **kwargs):
        id = 0
        context = super(IndexView, self).get_context_data(**kwargs)
        try:
            id = self.kwargs['id']
            if id == '0':
                note = self.queryset
            else:
                note = self.queryset.filter(tags__id=id)
        except:
            note = self.queryset
        paginator = Paginator(note, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            notes = paginator.page(page)
        except PageNotAnInteger:
            notes = paginator.page(1)
        except EmptyPage:
            notes = paginator.page(paginator.num_pages)
        context['tag'] = Tag.objects.all()
        context['note'] = notes
        context['selected_id'] = int(id)
        return context


# for notes page
class NotesListView(ListView):
    model = Note
    paginate_by = 10
    template_name = 'notes_app/list.html'


# for notes add and edit
def note_action(request, pk=None):
    if request.method == "POST":
        if pk is None:
            form = NoteForm(request.POST)
        else:
            notes = get_object_or_404(Note, pk=pk)
            form = NoteForm(request.POST, instance=notes)
        if form.is_valid():
            form.save()
            return HttpResponsePermanentRedirect(reverse('notes_app:index'))
    else:
        if pk is not None:
            notes = get_object_or_404(Note, pk=pk)
            form = NoteForm(instance=notes)
        else:
            form = NoteForm()
        return render(request, 'notes_app/add_note.html', {'form': form})


# for notes delete
def delete_note(request, pk):
    notes = get_object_or_404(Note, pk=pk)
    notes.delete()
    return HttpResponsePermanentRedirect(reverse('notes_app:index'))
