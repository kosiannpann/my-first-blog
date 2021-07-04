from django import forms
from .models import Post, Comment
from . import models

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('text',)
