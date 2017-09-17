from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.Index , name='index'),
	url(r'^posts/(?P<post_id>[0-9]+)/$',views.PostDetail, name='post_detail'),
	url(r'^category/(?P<category>([\w-])+)/$',views.CategoryIndex, name='category_index'),
	url(r'^new/$', views.NewPost, name='new_post'),
	url(r'^signup/$', views.SignUp, name='signup'),

	#url(r'^search/(?P<que>([\wd-])+)/$', views.SearchForum, name='forum_search'),
]