from cgitb import text
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, required=True)
    

    class Meta:
        model = Post
        fields = ('text', 'group')
        label = {
            'text': ('Текст поста'),
            'group': ('Группа поста')
        }
        help_texts = {
            'text': ('Текст нового поста'),
            'group': ('Группа, к которой будет относиться пост')
        }
