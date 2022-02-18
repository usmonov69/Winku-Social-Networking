from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import JsonResponse
from django.contrib import messages	
from django.views.generic import DeleteView, UpdateView 
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Like, PostView
from .forms import PostForm, PostUpdateForm, CommentForm
from profiles.models import Profile


@login_required
def post_comment_create_and_list_view(request):
	qs = Post.objects.all()
	recent_post = Post.objects.all()[:3]
	profile = Profile.objects.get(user=request.user)

	form = PostForm()
	form_c = CommentForm()
	if 'submit_p_form' in request.POST:
		form = PostForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = profile
			instance.save()
			form = PostForm()


	if 'submit_c_form' in request.POST:
		form_c = CommentForm(request.POST or None)
		# print(request.POST)
		if form_c.is_valid():
			instance = form_c.save(commit=False)
			instance.user = profile
			instance.post = Post.objects.get(id=request.POST.get('post_id'))
			instance.save()
			form_c = CommentForm()
	

	context = {
	'qs':qs,
	'profile':profile,
	'form':form,'form_c':form_c,
	'recent_post':recent_post}

	return render(request, 'index.html', context)

@login_required
def post_detail(request, pk):
	profile = Profile.objects.get(user=request.user)
	recent_post = Post.objects.all()[:3]
	obj = get_object_or_404(Post, pk=pk)

	if request.user.is_authenticated:
		PostView.objects.get_or_create(user=request.user, post=obj)

	form_c = CommentForm()

	if 'submit_c_form' in request.POST:
		form_c = CommentForm(request.POST or None)
		# print(request.POST)
		if form_c.is_valid():
			instance = form_c.save(commit=False)
			instance.user = profile
			instance.post = Post.objects.get(id=request.POST.get('post_id'))
			instance.save()
			form_c = CommentForm()

	context = {
	'obj':obj,
	'profile':profile,
	'form_c':form_c,
	'recent_post':recent_post
	}
	return render(request, 'posts/post_detail.html',context)


@login_required
def like_unlike_post(request):
	user = request.user
	if request.method == 'POST':
		post_id = request.POST.get('post_id')
		post_obj = Post.objects.get(id=post_id)
		profile = Profile.objects.get(user=user)

		if profile in post_obj.liked.all():
			post_obj.liked.remove(profile)
		else:
			post_obj.liked.add(profile)

		like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

	

		if not created:
			if like.value == 'Like':
				like.value = 'Unlike'
			else:
				like.value = 'Like'
		else:
			like.value = 'Like'

			post_obj.save()
			like.save()	
		data = {
		'value': like.value,
		'like': post_obj.liked.all().count()
		}
		# return JsonResponse(data, safe=False )
	return redirect ('posts:index')


class PostDeleteView(DeleteView, LoginRequiredMixin):
	model = Post
	template_name = 'posts/deletePost.html'
	success_url = reverse_lazy('posts:index')

	def get_objects(self, *args, **kwargs):
		pk = self.kwargs.get('pk')
		obj = Post.objects.get(pk=pk)
		if not obj.author.user == self.request.user:
			message.warning(self.request, "You need to be the author of the post in order to delete it")
		return obj 


class PostUpdateView(LoginRequiredMixin, UpdateView):
	form_class =PostUpdateForm
	model = Post
	template_name = 'posts/updatePost.html'
	success_url = reverse_lazy('posts:index')

	def form_valid(self, form):
		profile = Profile.objects.get(user=self.request.user)
		if form.instance.author == profile:
			return super().form_valid(form)
		else:
			form.add_error(None, "You need to be the author of the post in order to update it")
			return super().form_invalid(form)


@login_required
def post_update(request, id):
	content = get_object_or_404(Post, id=id)
	form = PostUpdateForm(request.POST or None, request.FILES or None, instance=content)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect('posts:index')
	context = {
	'form':form
	}
	return render(request, 'posts/updatePost.html', context)