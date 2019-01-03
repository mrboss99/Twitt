from django import forms
from .models import Post
from django.forms import CharField, ModelForm

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class PostForm(ModelForm):
    body = forms.Textarea()
    title = forms.CharField(max_length=200)

    class Meta:
        model = Post
        fields = ['body', 'title',]

