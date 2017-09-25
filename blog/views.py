from django.shortcuts import render,HttpResponse
from blog.models import Category, Tag, Post
# Create your views here.

def index(request):
    #return HttpResponse('thanks')
    post_list = Post.objects.all().order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})
