from django import forms

from .models import ForumPost, Comment, Messages, PostCategory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
	topic = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	text = forms.CharField(widget=forms.Textarea(attrs={'rows':'5', 'cols':'50','class':'form-control'}))
	class Meta:
		model = ForumPost
		fields = ('topic', 'text','category')


class SignUpForm(UserCreationForm):
	first_name=forms.CharField(max_length=25,required=True, widget=forms.TextInput(attrs={'style':'text-transform:capitalize;',}))
	last_name=forms.CharField(max_length=25, required=True, widget=forms.TextInput(attrs={'style':'text-transform:capitalize;',}))
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
	comment = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	class Meta:
		model = Comment
		fields = ('comment',)

class MessageForm(forms.ModelForm):
	message=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control',}))
	class Meta:
		model = Messages
		fields = ('message',)