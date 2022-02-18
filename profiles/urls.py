from django.urls import path 

from . import views

app_name = 'profiles' 

urlpatterns = [
	path('', views.ProfileListView.as_view(), name="profiles-list-view"),
	path('search/', views.search, name='search-profile'),
	# path('myprofile/', views.my_profile, name='my-profile'),
	path('myprofile/', views.edit_profile, name='my-profile'),
	# path('myinvite/', views.invites_receved_view, name='invites-receved-view'),
	path('my-invites/', views.invites_receved_view, name='my-invites-view'),
	path('to-invite/', views.invite_profiles_list_view, name='to-invite-profiles'),
	path('send_invat/', views.send_invatation, name='send_inva'),
	path('remove_friends/', views.remove_from_friends, name='remove-friends'),
	path('<slug>/', views.ProfileDetailView.as_view(), name='profile-detail-view'),
	path('my-invites/accept/', views.accept_invatation, name='accept-invite'),
	path('my-invites/reject/', views.reject_invatation, name='reject-invite'),


]
