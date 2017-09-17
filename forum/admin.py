# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import PostCategory, ForumPost, Comment

admin.site.register(PostCategory)
admin.site.register(ForumPost)
admin.site.register(Comment)