from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Post
        fields = ('group', 'text', 'image') 
        label = {
            'text': ('Текст поста'),
            'group': ('Группа поста'),
            'image': ('Изображение')
        }
        help_texts = {
            'text': ('Текст нового поста'),
            'group': ('Группа, к которой будет относиться пост'),
            'image': ('Выберите изображение')
        }
