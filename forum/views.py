# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .models import ForumPost, PostCategory

# Create your views here.

def Index(request):
	latest_posts=ForumPost.objects.order_by('-date')[:5]
	output = '<hr>'.join(["Topic: <a href = './"+str(fp.id)+"'> " + fp.topic + "</a> <br> Posted in: <a href = './category/"+str(fp.category) + "'>" + str(fp.category.name) + "</a> <br> Posted On : " + str(fp.date) 
 		for fp in latest_posts])
	return HttpResponse(output)

def PostDetail(request,post_id):
	current_post=ForumPost.objects.filter(id=int(post_id))[:1].get()
	return HttpResponse("Hello You are on a particular post with post id = "+current_post.text)

def CategoryIndex(request, category):
	get_cat_id = PostCategory.objects.order_by('-date')[:5]
	latest_posts_in_cat=ForumPost.objects.order_by('-date')[:5]
	output = '<hr>'.join(["Topic: <a href = './"+str(fp.id)+"'> " + fp.topic + "</a> <br> Posted On : " + str(fp.date) 
 		for fp in latest_posts_in_cat])
	return HttpResponse(output)