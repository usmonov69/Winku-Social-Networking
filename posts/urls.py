from django.urls import path 

from . import views

app_name = "posts"

urlpatterns = [
	path('', views.post_comment_create_and_list_view, name='index'),
	# path('posts', views.post_comment_create_and_list_view, name='main-post-view'),
	path('like_unlike_post', views.like_unlike_post, name='like-unlike-post'),
	path('<pk>/delete', views.PostDeleteView.as_view(), name='delete-post'),
	# path('<pk>/update', views.PostUpdateView.as_view(), name='update-post'),
	path('<id>/update', views.post_update, name='update-post'),
	path('<pk>/detail', views.post_detail, name='post-detail')
] 