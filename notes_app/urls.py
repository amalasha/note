from django.urls import path
from notes_app import views
from notes_app.models import Note, Tag

# SET THE NAMESPACE!
app_name = 'notes_app'

urlpatterns = [
    path('index/',views.IndexView.as_view(),name='index'),
    path('index/<id>',views.IndexView.as_view(),name='index'),
    path('note_action/', views.note_action, name='note_action'),
    path('note_action/<pk>', views.note_action, name='note_action'),
    path('delete_note/<pk>', views.delete_note, name='delete_note'),
    path('tag/', views.TagsListView.as_view(queryset=Tag.objects.all()), name='tag'),
    path('tag_action/', views.tag_action, name='tag_action'),
    path('tag_action/<pk>', views.tag_action, name='tag_action'),
    path('delete_tag/<pk>', views.delete_tag, name='delete_tag'),
    path('ajax/addtag',views.addtag, name='addtag'),

    path('home/',views.home,name='homepage'),
    path('home/<id>',views.home,name='homepage'),


    path('', views.NotesListView.as_view(queryset=Note.objects.all().order_by("-created_date")), name='home'),

]
