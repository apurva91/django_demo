from __future__ import unicode_literals
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, authenticate
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.utils import timezone
from django.core import serializers
from django.http import HttpResponse, Http404, JsonResponse
from .models import ForumPost, PostCategory, Comment, Messages, LastMsg
from .forms import PostForm, SignUpForm, CommentForm, EditProfileForm, MessageForm
# Create your views here.
import logging
logger = logging.getLogger(__name__)
# import the logging library, Log an error message
#logger.error('Something went wrong!')

def SignUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.birth_date=form.cleaned_data.get('birth_date')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'forum/signup.html', {'form': form})

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
	#Adding New Posts Should be only available to users
	if request.user.is_authenticated:
		if request.method=='POST':
			form = PostForm(request.POST)
			if form.is_valid():
				post = form.save(commit=False)
				post.date = timezone.now()
				post.author = request.user
				post.save()
				return redirect('/posts/'+str(post.id))
		else:
			form = PostForm()
		return render(request, 'forum/index.html', {'latest_posts':latest_posts, 'form':form})
	else:
		return render(request, 'forum/index.html', {'latest_posts':latest_posts})

def PostDetail(request,post_id):

	current_post = get_object_or_404(ForumPost, pk=post_id)
	form = CommentForm()
	form2 = PostForm(initial={'topic':current_post.topic,'text':current_post.text,'category':current_post.category,})
	current_post_comments = Comment.objects.filter(forumpost=current_post.id).order_by('-date')
	if request.user.is_authenticated:
		if request.method == 'POST':
			if 'Comment' in request.POST:
				form = CommentForm(request.POST)
				if form.is_valid():
					comment = form.save(commit=False)
					comment.date = timezone.now()
					comment.author = request.user
					comment.forumpost = current_post
					comment.save()
					return redirect('/posts/'+str(current_post.id))
			elif 'Delete' in request.POST:
				ForumPost.objects.filter(pk=post_id).delete()
				return redirect('/profile/'+str(current_post.author))
			elif 'Edit' in request.POST:
				form2 = PostForm(request.POST,instance=current_post)
				if form2.is_valid():
					current_post = form2.save()
					current_post.save()
					return redirect('/posts/'+str(current_post.id))

	return render(request,'forum/post_detail.html',{'current_post':current_post, 'current_post_comments':current_post_comments, 'form':form,'form2':form2,})

def CategoryIndex(request, category):

	latest_posts_in_cat=ForumPost.objects.filter(category__url=category).order_by('-date')
	if latest_posts_in_cat.count()==0:
		raise Http404("Category Not Found")
	paginator = Paginator(latest_posts_in_cat, 5)

	page = request.GET.get('page')
	try:
		latest_posts_in_cat = paginator.page(page)
	except PageNotAnInteger:
		latest_posts_in_cat = paginator.page(1)
	except EmptyPage:
		latest_posts_in_cat = paginator.page(paginator.num_pages)

	return render(request, 'forum/category_index.html', {'latest_posts_in_cat':latest_posts_in_cat})

def SearchForum(request):
	que = request.GET.get('q')
	query=ForumPost.objects.filter(Q(text__contains=que)|Q(topic__contains=que)).order_by('-date')
	paginator = Paginator(query, 5) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
		query = paginator.page(page)
	except PageNotAnInteger:
		query = paginator.page(1)
	except EmptyPage:
		query = paginator.page(paginator.num_pages)

	return render(request,'forum/search.html',{'query':query, 'que':que})

def Profile(request,user):
	try :
		user_data=User.objects.filter(username=user).get()
	except User.DoesNotExist:
		raise Http404("User Not Found")
	
	if request.user.is_authenticated:
		r_user_data=User.objects.filter(username=request.user).get()
	else:
		raise Http404("You Must LogIn To View Profile")
	
	if user_data.id==r_user_data.id:
	 	user_post=ForumPost.objects.filter(author__username=user).order_by('-date')[:5]
	 	
	 	if request.method=='POST':
			form = EditProfileForm(request.POST,instance=user_data)
		
			if form.is_valid():
				user_data = form.save()
				user_data.save()
				return redirect('/profile/'+str(user))
		else:
			form = EditProfileForm(initial={'first_name': user_data.first_name,'last_name': user_data.last_name,'email': user_data.email,})
		return render(request, 'forum/user_profile.html', {'user_post':user_post,'user_data':user_data, 'form':form})
	else:
		user_post=ForumPost.objects.filter(author__username=user).order_by('-date')[:5]
		return render(request, 'forum/profile.html', {'user_post':user_post,'user_data':user_data})

def SendShowMsg(request,reciever):
	try :
		reciever=User.objects.filter(username=reciever).get()
	except User.DoesNotExist:
		raise Http404("User Not Found")
	if request.user.is_authenticated:
		sender=User.objects.filter(username=request.user).get()
	else:
		raise Http404("You Must LogIn To View Profile")
	all_msg = Messages.objects.filter((Q(user2=sender.id)&Q(user1=reciever.id))|(Q(user1=sender.id)&Q(user2=reciever.id))).order_by('-date')
	form = MessageForm()
	if request.method=='POST':
		form = MessageForm(request.POST)
		if form.is_valid():
			newmessage = form.save(commit=False)
			newmessage.date = timezone.now()
			newmessage.user1 = sender
			newmessage.user2 = reciever
			newmessage.save()
			lastmsg=LastMsg.objects.filter((Q(user2=sender.id)&Q(user1=reciever.id))|(Q(user1=sender.id)&Q(user2=reciever.id))).order_by('-date').first()
			if lastmsg:
				lastmsg.date=newmessage.date
				lastmsg.user1 = sender
				lastmsg.user2 = reciever
				lastmsg.message=newmessage.message
				lastmsg.save()
			else :
				lastmsg=LastMsg.objects.create(user1=sender,user2=reciever,message=newmessage.message,date=newmessage.date)
			return redirect('/messages/'+str(reciever))

	return render(request,'forum/message.html',{'reciever':reciever,'form':form,'all_msg':all_msg})

def MsgRefresh(request,reciever):
	reciever=User.objects.filter(username=reciever).get()
	sender=User.objects.filter(username=request.user).get()
	all_msg = Messages.objects.filter((Q(user2=sender.id)&Q(user1=reciever.id))|(Q(user1=sender.id)&Q(user2=reciever.id))).order_by('-date')
	msg_json = serializers.serialize('json', all_msg)
	return JsonResponse(msg_json,safe=False)
	#return HttpResponse(all_msg)



def MsgIndex(request):
	if request.user.is_authenticated:
		sender=User.objects.filter(username=request.user).get()
	else:
		raise Http404("You Must Login First")

	all_msg= LastMsg.objects.filter(Q(user2=sender.id)|Q(user1=sender.id)).order_by('-date')
	#all_msg = Messages.objects.filter(Q(user2=sender.id)|Q(user1=sender.id)).order_by('-date')
	return render(request,'forum/msgindex.html',{'all_msg':all_msg})
def MsgIRefresh(request):
	if request.user.is_authenticated:
		sender=User.objects.filter(username=request.user).get()
	else:
		raise Http404("You Must Login First")

	all_msg= LastMsg.objects.filter(Q(user2=sender.id)|Q(user1=sender.id)).order_by('-date')
	msg_json = serializers.serialize('json', all_msg)
	return JsonResponse(msg_json, safe=False)

