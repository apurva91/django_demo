# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from tinymce.models import HTMLField
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
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    topic = models.CharField(max_length=255)
    #text = models.CharField(max_length=1000)
    text = HTMLField()
    date = models.DateTimeField('date')
    category = models.ForeignKey( PostCategory, on_delete = models.CASCADE )

    def __str__(self):
        return self.topic

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.CharField(max_length=1000)
    date = models.DateTimeField('date')
    forumpost = models.ForeignKey(ForumPost, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.author) + '\'s comment on ' + str(self.forumpost)

class Messages(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    user2 = models.ForeignKey(  User, on_delete=models.CASCADE, related_name='reciever')
    date = models.DateTimeField('date')
    message = models.CharField(max_length=1000)
    def __str__(self):
        return self.user1
    def __unicode__(self):
        return self.user1
    def __str__(self):
        return self.user2
    def __unicode__(self):
        return self.user2e
    def __str__(self):
        return self.message
    def __unicode__(self):    
        return self.message

class LastMsg(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lsender')
    user2 = models.ForeignKey(  User, on_delete=models.CASCADE, related_name='lreciever')
    date = models.DateTimeField('date')
    message = models.CharField(max_length=1000)
    msg_read = models.BooleanField()
    def __str__(self):
        return self.user1
    def __unicode__(self):
        return self.user1
    def __str__(self):
        return self.user2
    def __unicode__(self):
        return self.user2
    def __str__(self):
        return self.message
    def __unicode__(self):    
        return self.message
    def __str__(self):
        return self.msg_read


