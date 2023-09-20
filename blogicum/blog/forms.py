from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

from .validators import is_username_english

from .models import Post, Comment


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)

        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format="%Y-%m-%d %H:%M:%S"
            ),
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


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()

    def clean_username(self):
        username = self.cleaned_data['username']
        is_username_english(username)

        return username

