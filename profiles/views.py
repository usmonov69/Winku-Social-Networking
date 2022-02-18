from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
 
from .models import Profile, Relationship
from posts.models import Post
from .forms import ProfileForm




def my_profile(request):
	profile = Profile.objects.get(user=request.user)
	context = {'profile':profile}
	return render(request, 'test.html', context)

@login_required
def search(request):
	queryset  = Profile.objects.all()
	query = request.GET.get('q')
	if query:
		queryset = queryset.filter(
		Q(user__username__icontains=query)).distinct()
		# print("=========",queryset)
	context = {
	'queryset': queryset,
	}
	return render(request, 'search_results.html', context)


@login_required
def edit_profile(request):
	profile = Profile.objects.get(user=request.user)
	form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
	confirm = False
	if form.is_valid():
		form.save()
		confirm = True 
	context={'profile':profile, 'form':form}
	return render(request, 'edit_profile.html', context)

# bu bizga kelgan yani user-lar bizga follow yuborsa kim yuborganini chiqaradi 
@login_required
def invites_receved_view(request):
	profile = Profile.objects.get(user=request.user)
	qs = Relationship.objects.invatations_received(profile)
	results = list(map(lambda x : x.sender, qs))
	is_empty = False
	if len(results) == 0:
		is_empty = True
	count = len(results)
	context = {
	'qs': results,
	'is_empty': is_empty,
	'count':count,
	'profile':profile
	}
	return render(request, 'my_invites.html', context)

@login_required
def invite_profiles_list_view(request):
	user = request.user
	qs = Profile.objects.get_all_profiles_to_invite(user)
	profile = Profile.objects.get(user=user)

	context = {
	'qs': qs,
	'profile':profile,
	}
	return render(request, 'to_invite_profile.html', context)

@login_required
def profiles_list_view(request):
	user = request.user
	qs = Profile.objects.get_all_profiles(user)

	context = {
	'qs': qs,
	}
	return render(request, 'prosfile_list.html', context)
@login_required
def accept_invatation(request):
	if request.method == 'POST':
		pk = request.POST.get('profile_pk')
		sender = Profile.objects.get(pk=pk)
		receiver = Profile.objects.get(user=request.user)
		rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
		if rel.status =='send':
			rel.status = 'accepted'
			rel.save()
		return redirect('profiles:my-invites-view')
@login_required
def reject_invatation(request):
	if request.method == 'POST':
		pk  = request.POST.get('profile_pk')
		sender = Profile.objects.get(pk=pk)
		receiver = Profile.objects.get(user=request.user)
		rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
		rel.delete()
	return redirect("profiles:my-invites-view")


class ProfileDetailView(LoginRequiredMixin, DetailView):
	model = Profile
	template_name = 'profile_detail.html'

	# def get_object(self , slug=None):
	# 	slug = self.kwargs.get('slug')
	# 	profile = Profile.objects.get(slug=slug)
	# 	return profile

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		post = Post.objects.all()
		user = User.objects.get(username__iexact=self.request.user)
		profile = Profile.objects.get(user=user)
		friends = self.get_object().get_friends()
		rel_r = Relationship.objects.filter(sender=profile)
		rel_s = Relationship.objects.filter(receiver=profile)
		rel_receiver = []
		rel_sender = []
		for item in rel_r:
			rel_receiver.append(item.receiver.user)
		for item in rel_s:
			rel_sender.append(item.sender.user)
		context['rel_receiver'] = rel_receiver
		context['rel_sender'] = rel_sender
		context['friends'] = friends
		context['posts'] = self.get_object().get_all_authors_posts()
		context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False
		return context

class ProfileListView(LoginRequiredMixin, ListView ):
	model = Profile
	template_name ='profile_list.html'
	# context_object_name = 'qs'

	def get_queryset(self):
		qs = Profile.objects.get_all_profiles(self.request.user)
		return qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = User.objects.get(username__iexact=self.request.user)
		profile = Profile.objects.get(user=user)
		rel_r = Relationship.objects.filter(sender=profile)
		rel_s = Relationship.objects.filter(receiver=profile)
		rel_receiver = []
		rel_sender = []
		for item in rel_r:
			rel_receiver.append(item.receiver.user)
		for item in rel_s:
			rel_sender.append(item.sender.user)
		context['rel_receiver'] = rel_receiver
		context['rel_sender'] = rel_sender
		context['profile'] = profile
		context['is_empty'] = False
		# if len(self.get_queryset()) == 0:
		# 	context['is_empty'] = True

		return context
@login_required
def send_invatation(request):
	if request.method == 'POST':
		pk = request.POST.get('profile_pk')
		# user = request.user
		sender = Profile.objects.get(user=request.user)
		receiver = Profile.objects.get(pk=pk)

		rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

		return redirect(request.META.get("HTTP_REFERER"))	
	return redirect('profiles:my-profile')


@login_required
def remove_from_friends(request):
	if request.method == 'POST':
		pk = request.POST.get('profile_pk')
		user = request.user
		sender = Profile.objects.get(user=user)
		receiver = Profile.objects.get(pk=pk)

		rel = Relationship.objects.get(
			(Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
			)
		rel.delete()
		return redirect(request.META.get("HTTP_REFERER"))	
	return redirect('profiles:my-profile-view')
 

