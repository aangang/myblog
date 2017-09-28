from django.shortcuts import render,HttpResponse,get_object_or_404
from blog.models import Category, Tag, Post
import markdown
from comments.forms import CommentForm
# Create your views here.

from django.views.generic import ListView


def index(request):
    #return HttpResponse('thanks')
    print("index")
    post_list = Post.objects.all().order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

#使用列表视图类
#参数:
#model。将 model 指定为 Post，告诉 Django 我要获取的模型是 Post。
#template_name。指定这个视图渲染的模板。
#context_object_name。指定获取的模型列表数据保存的变量名。这个变量会被传递给模板。
#怎么排序呢？
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    

def detail(request,pk):
    #return HttpResponse('thanks')
    print("detail")
    post = get_object_or_404(Post,pk=pk)
    # 阅读量 +1
    post.increase_views()
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    # 记得在顶部导入 CommentForm
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()
    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'post': post,
               'form': form,
               'comment_list': comment_list
               }
    return render(request,'blog/detail.html',context=context)




def archives(request,year,month):
    #return HttpResponse('thanks')
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

def get_categories(request,category_id):
    post_list = Post.objects.filter(category_id=category_id).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})






