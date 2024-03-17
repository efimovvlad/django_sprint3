from django.shortcuts import render, get_object_or_404, get_list_or_404
from blog.models import Post, Category
from django.utils import timezone


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )[:5]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, pk):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related(
            'category'
        ).filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        ),
        pk=pk
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    post_list = get_list_or_404(
        Post.objects.select_related(
            'category',
            'location',
            'author'
        ).filter(
            category__slug=category_slug,
            is_published=True,
            pub_date__lte=timezone.now()
        ), category__is_published=True
    )
    category = get_object_or_404(Category, slug=category_slug)
    context = {'post_list': post_list, 'category': category}
    return render(request, template, context)
