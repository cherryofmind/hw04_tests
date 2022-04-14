from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django import forms

from ..forms import PostForm
from ..models import Group, Post


User = get_user_model()

class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.new_user = User.objects.create_user(username='auth')
        cls.new_user_client = Client()
        cls.new_user_client.force_login(cls.new_user)

        cls.group = Group.objects.create(
            title='group',
            slug='test_slug',
            description='Описание',
        )
        cls.post = Post.objects.create(
            author=cls.new_user,
            text='Тестовый пост',
            group=cls.group,
        )
        # Создаем форму, если нужна проверка атрибутов
        cls.form = PostForm()


    def test_form_create_post(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()
        form_data = {
                'text': 'second text',
        }
        response = self.new_user_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count+1)