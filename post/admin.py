from django.contrib import admin
from django_summernote.widgets import SummernoteWidget
from .models import Post, Tag
from django.db import models

class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': SummernoteWidget()}
    }

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)