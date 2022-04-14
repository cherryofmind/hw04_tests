from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User
from .forms import PostForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Отдаем в словаре контекста
    context = {
        'page_obj': page_obj,
        'posts': post_list,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'group': group,
        'posts': post_list,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = User.objects.get(username=username)
    author_post = Post.objects.filter(author=author).order_by('-pub_date')
    posts_numbers = author_post.count()
    paginator = Paginator(author_post, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'author': author,
        'author_post': author_post,
        'posts_numbers': posts_numbers,

    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.select_related('author', 'group').get(id=post_id)
    post_count = Post.objects.filter(author=post.author).count()
    post_list = post.author.posts.all()
    context = {
        'post_list': post_list,
        'post': post,
        'post_count': post_count,

    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect('posts:profile', request.user)
    form = PostForm()
    return render(request, 'posts/post_create.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_edit = True
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    if request.method == 'POST':
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect('posts:post_detail', post_id)
    form = PostForm(instance=post)
    return render(request, 'posts/post_create.html', {'form': form,
                  'is_edit': is_edit})
