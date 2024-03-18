from django.shortcuts import render, get_object_or_404, get_list_or_404
from blog.models import Post, Category
from django.utils import timezone
from blog.constants import number_of_posts


def search_params():
    data = Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )
    return data


def index(request):
    template = 'blog/index.html'
    post_list = search_params()[:number_of_posts]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, pk):
    template = 'blog/detail.html'
    post = get_object_or_404(
        search_params(),
        pk=pk
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    post_list = get_list_or_404(
        search_params().filter(
            category__slug=category_slug
        ), category__is_published=True
    )
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )
    context = {'post_list': post_list, 'category': category}
    return render(request, template, context)
