from django.shortcuts import render
from .models import Post
# Create your views here.
def blog1(request):
    data=Post.objects.all()
    return render(request,'blog/page-blog-grid.html',{'data':data})


    
def blogPost(request, slug):
    post=Post.objects.get(slug=slug)
    title=post.title
    author=post.author
    content=post.content
    img=post.img
    return render(request, 'blog/blogPost.html',{'title':title,'author':author,'content':content,'img':img})