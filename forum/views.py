# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import ForumPost, PostCategory

# Create your views here.

def Index(request):
	latest_posts=ForumPost.objects.order_by('-date')[:5]
	return render(request, 'forum/index.html', {'latest_posts':latest_posts})

def PostDetail(request,post_id):

	current_post = get_object_or_404(ForumPost, pk=post_id)
	return render(request,'forum/post_detail.html',{'current_post':current_post})

def CategoryIndex(request, category):

	latest_posts_in_cat=ForumPost.objects.filter(category__url=category).order_by('-date')[:5]
	if latest_posts_in_cat.count()==0:
		raise Http404("Category Not Found")
	return render(request, 'forum/category_index.html', {'latest_posts_in_cat':latest_posts_in_cat})