from django import forms 
from .models import Post, Comment

class PostForm(forms.ModelForm):
	content  = forms.CharField(widget=forms.Textarea(attrs={'rows':2,"placeholder":"write something..." }))
	class Meta:
		model = Post
		fields = ('content', 'image')



class PostUpdateForm(forms.ModelForm):
	content  = forms.CharField(widget=forms.Textarea(attrs={'rows':10,"placeholder":"write something..." }))
	class Meta:
		model = Post
		fields = ('content', 'image')


class CommentForm(forms.ModelForm):
	body = forms.CharField(label='',
							 widget=forms.TextInput(attrs={"placeholder":"Add a comments here..."}))
	class Meta:
		model = Comment
		fields = ('body',)
