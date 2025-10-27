from django.shortcuts import render, get_object_or_404
from .models import Post, Category


def blog_list(request):
    category_slug = request.GET.get('category')
    posts = Post.objects.filter(is_published=True)
    categories = Category.objects.all()
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    return render(request, 'blog_list.html', {
        'posts': posts,
        'categories': categories,
        'active_category': category_slug,
    })


def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, 'blog_detail.html', {'post': post})
