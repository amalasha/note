from django.contrib import admin

# Register your models here.
from notes_app.models import Note, Tag
admin.site.register(Note)
admin.site.register(Tag)