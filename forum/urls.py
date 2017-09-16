from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.Index , name='index'),
	url(r'^([0-9]+)/$',views.PostDetail, name='post_detail'),
	url(r'^category/(?P<category>([\w-])+)/$',views.CategoryIndex, name='category_index'),
	url(r'^new/$', views.NewPost, name='new_post'),
]