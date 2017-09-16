from __future__ import unicode_literals
# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse, Http404
from .models import ForumPost, PostCategory
from .forms import PostForm
from django.db.models import Q
# Create your views here.

def Index(request):
	latest_posts=ForumPost.objects.order_by('-date')
	paginator = Paginator(latest_posts, 5) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
		latest_posts = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		latest_posts = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		latest_posts = paginator.page(paginator.num_pages)


	return render(request, 'forum/index.html', {'latest_posts':latest_posts})

def PostDetail(request,post_id):

	current_post = get_object_or_404(ForumPost, pk=post_id)
	return render(request,'forum/post_detail.html',{'current_post':current_post})

def CategoryIndex(request, category):

	latest_posts_in_cat=ForumPost.objects.filter(category__url=category).order_by('-date')[:5]
	if latest_posts_in_cat.count()==0:
		raise Http404("Category Not Found")
	paginator = Paginator(latest_posts_in_cat, 5) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
		latest_posts_in_cat = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		latest_posts_in_cat = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		latest_posts_in_cat = paginator.page(paginator.num_pages)


	return render(request, 'forum/category_index.html', {'latest_posts_in_cat':latest_posts_in_cat})

#def SearchForum(request, que):
#	query=ForumPost.objects.filter(Q(text__search=que) | Q(topic__search=que)).order_by('-date')
#	return HttpResponse(query.count())

def NewPost(request):
	if request.method=='POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.date = timezone.now()
			post.save()
			return redirect('/posts/'+str(post.id))
	else:
		form = PostForm()

	return render(request, 'forum/post_edit.html', {'form': form})
    	

