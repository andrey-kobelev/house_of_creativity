from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

from .models import Post, Comment


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)

        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'}),
        }


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea({'cols': '22', 'rows': '5'})
        }


class ProfileForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email']
