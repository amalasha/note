import pytest
from notes_app.models import Note, Tag
from django.urls import reverse
import json

pytestmark = pytest.mark.django_db


class TestModel:
    def test_tag_save(self):
        tag = Tag.objects.create(
            tag="test tag"
        )
        assert tag.id == 1
        assert 'test tag' == str(tag)

    def test_note_save(self):
        note = Note.objects.create(
            note="Sample note",
        )
        note.tags.add(1)
        assert note.note == 'Sample note'
        assert 'Sample note' == str(note)


class TestViewTag:

    def test_delete_tag(self, client):
        response = client.get(reverse('notes_app:delete_tag', kwargs={'pk': 2}))
        assert response.status_code == 404
        tag = Tag.objects.create(
            tag="test tag"
        )
        response = client.get(reverse('notes_app:delete_tag', kwargs={'pk': 1}))
        assert 301 == response.status_code
        assert '/tag/' in str(response)

    def test_add_tag(self, client):
        response = client.post('/ajax/addtag', data={'tag': 'test'})
        assert 200 == response.status_code

    def test_tag_action(selfself, client):
        response = client.post('/tag_action', {'tag': 'example'})
        assert 301 == response.status_code
        assert '/tag_action/' in str(response)

        response = client.get('/tag_action', {'tag': 'update example', 'id': 1})
        assert 301 == response.status_code
        assert '/tag_action/' in str(response)


class TestViewNote:
    def test_delete_note(self, client):
        response = client.post(reverse('notes_app:delete_note', kwargs={'pk': 2}))
        assert response.status_code == 404
        note = Note.objects.create(
            note="Sample note",
        )
        response = client.get(reverse('notes_app:delete_note', kwargs={'pk': 1}))
        assert 301 == response.status_code
        assert '/home/' in str(response)

    def test_note_action(selfself, client):
        response = client.post('/note_action', {'note': 'example'})
        assert 301 == response.status_code
        assert '/note_action/' in str(response)

        response = client.get('/note_action', {'note': 'update example', 'id': 1}, kwargs={'pk': 1})
        assert 301 == response.status_code
        assert '/note_action/' in str(response)


class TestView:
    def test_home_view(self, client):
        response = client.get(reverse('notes_app:home'))
        assert response.status_code == 200

    def test_notes_pagination(self, client):
        response = client.get(reverse('notes_app:home', kwargs={'id': 2}))
        assert 'Page 1 of 1' in str(response.context['note'])


    def test_tag_list_view(selfself, client):
        response = client.get(reverse('notes_app:tag'))
        assert response.status_code == 200
