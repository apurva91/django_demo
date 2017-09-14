# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class PostCategory(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'post categories'	

class ForumPost(models.Model):
	topic = models.CharField(max_length=255)
	text = models.CharField(max_length=1000)
	date = models.DateTimeField(' date published ')
	category = models.ForeignKey( PostCategory, on_delete = models.CASCADE )

	def __str__(self):
		return self.topic