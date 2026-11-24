from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .constants import POSTS_ON_INDEX
from .models import Category, Post


def filter_posts_by_publication(posts):
    """Оставляет только опубликованные посты."""
    return posts.select_related(
        'category', 'location', 'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now(),
    )


def index(request):
    post_list = filter_posts_by_publication(
        Post.objects.all()
    )[:POSTS_ON_INDEX]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, post_id):
    post = get_object_or_404(
        filter_posts_by_publication(Post.objects.all()),
        pk=post_id,
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    return render(request, 'blog/category.html', {
        'category': category,
        'post_list': filter_posts_by_publication(category.posts.all()),
    })
