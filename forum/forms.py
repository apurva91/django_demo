from django import forms

from .models import ForumPost

class PostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ('topic', 'text','category')