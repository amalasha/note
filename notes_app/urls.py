from django.urls import path
from notes_app import views
from notes_app.models import Note, Tag

# SET THE NAMESPACE!
app_name = 'notes_app'

urlpatterns = [
    path('', views.NotesListView.as_view(queryset=Note.objects.all().order_by("-created_date")), name='home'),
    path('note_action/', views.note_action, name='note_action'),
    path('note_action/<pk>', views.note_action, name='note_action'),
    path('tag/', views.tag, name='tag'),
    path('delete_note/<pk>', views.delete_note, name='delete_note'),

]
