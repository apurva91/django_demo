from django import forms

from .models import ForumPost, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
	text = forms.CharField(widget=forms.Textarea(attrs={'rows':'5', 'cols':'50','overflow-y':'scroll'}))
	class Meta:
		model = ForumPost
		fields = ('topic', 'text','category')


class SignUpForm(UserCreationForm):
	first_name=forms.CharField(max_length=25,required=True)
	last_name=forms.CharField(max_length=25, required=True)
	email=forms.EmailField(max_length=100, required=True)
	birth_date=forms.DateField(widget=forms.TextInput(attrs={'id':'datepicker'}))
	class Meta:
		model = User
		fields=('username','first_name','last_name','birth_date','email','password1','password2',)

class EditProfileForm(forms.ModelForm):
	first_name=forms.CharField(max_length=25)
	last_name=forms.CharField(max_length=25)
	email=forms.EmailField(max_length=100)
	class Meta:
		model = User
		fields=('first_name','last_name','email',)

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('comment',)

