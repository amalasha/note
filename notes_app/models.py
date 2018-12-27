from django.db import models

# Create your models here.
class Note(models.Model):
    note = models.TextField(max_length=2000)
    created_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='tags', blank=True)

    def __unicode__(self):
        return self.note


class Tag(models.Model):
    tag = models.CharField(max_length=200)

    def __unicode__(self):
        return self.tag

