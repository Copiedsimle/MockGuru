from django.shortcuts import render, get_object_or_404
from .models import BlogPost

def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True, post_type='blog')
    return render(request, 'blog/blog_list.html', {'posts': posts})

def notes_list(request):
    notes = BlogPost.objects.filter(is_published=True, post_type='notes')
    return render(request, 'blog/notes_list.html', {'notes': notes})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True, post_type='blog')
    return render(request, 'blog/blog_detail.html', {'post': post})

def notes_detail(request, slug):
    note = get_object_or_404(BlogPost, slug=slug, is_published=True, post_type='notes')
    return render(request, 'blog/notes_detail.html', {'note': note})
