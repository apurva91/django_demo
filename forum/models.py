# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class PostCategory(models.Model):
    name = models.CharField(max_length=255)
    url = models.SlugField()
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.url = slugify(self.name)
        super(PostCategory, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.url
    
    class Meta:
        verbose_name_plural = 'post categories'	

class ForumPost(models.Model):
	topic = models.CharField(max_length=255)
	text = models.CharField(max_length=1000)
	date = models.DateTimeField('date')
	category = models.ForeignKey( PostCategory, on_delete = models.CASCADE )

	def __str__(self):
		return self.topic