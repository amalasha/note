from django.shortcuts import render
from django.views.generic import ListView
from notes_app.models import Note, Tag
from notes_app.forms import NoteForm, TagForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json
import logging
logger = logging.getLogger(__name__)

class TagsListView(ListView):
    """
    Lists tags
    """
    model = Tag
    paginate_by = 10
    template_name = 'notes_app/tag.html'


def tag_action(request, pk=None):
    """
        Tag edit
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
    Tag addition
    """
    if request.method == 'POST':
        tag = request.POST["tag"]
        t = Tag.objects.create(tag=tag)
        response_data = {}
        response_data['id'] = t.pk
        response_data['tag'] = t.tag
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def delete_tag(request, pk):
    """
    Tag deletion
    """
    tags = get_object_or_404(Tag, pk=pk)

    tags.delete()

    return HttpResponsePermanentRedirect(reverse('notes_app:tag'))


def home(request, id='0'):
    """
        Homepage showing notes and tags
    """
    form = NoteForm()
    if id is None or id == '0':
        notes_list = Note.objects.all().order_by('-created_date')
    else:
        notes_list = Note.objects.filter(tags__id=id).order_by('-created_date')
    tag_list = Tag.objects.all()
    paginator = Paginator(notes_list, 10)
    page = request.GET.get('page')
    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)
    return render(request, 'notes_app/list.html',
                  {'note': notes, 'tag': tag_list, 'selected_id': int(id), 'form': form})


def note_action(request, pk=None):
    """
        Notes add and edit
    """

    if request.method == "POST":
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
    """
        Notes deletion
    """
    notes = get_object_or_404(Note, pk=pk)
    notes.delete()
    return HttpResponsePermanentRedirect(reverse('notes_app:home'))
