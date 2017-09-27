from django.shortcuts import render,HttpResponse,get_object_or_404
from blog.models import Category, Tag, Post
import markdown
# Create your views here.

def index(request):
    #return HttpResponse('thanks')
    post_list = Post.objects.all().order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

def detail(request,pk):
    #return HttpResponse('thanks')
    post = get_object_or_404(Post,pk=pk)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    return render(request,'blog/detail.html',context={'post':post})




def archives(request,year,month):
    #return HttpResponse('thanks')
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})









