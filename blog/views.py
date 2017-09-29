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
#怎么排序呢？覆写get_queryset函数
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 6
    def get_queryset(self):
        return super(IndexView, self).get_queryset().all().order_by('-created_time')

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


def get_categories(request,category_id):
    post_list = Post.objects.filter(category_id=category_id).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

#category 视图函数中多了一步，即首先需要根据从 URL 中捕获的分类 id 并从数据库获取分类，然后使用 filter 函数过滤出该分类下的全部文章
#覆写了父类的get_queryset 方法。该方法默认获取指定模型的全部列表数据。为了获取指定分类下的文章列表数据，我们覆写该方法，改变它的默认行为
class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('category_id'))
        return super(CategoryView, self).get_queryset().filter(category=cate
                                                            ).order_by('-created_time')


def archives(request,year,month):
    #return HttpResponse('thanks')
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    def get_queryset(self):
        return super(ArchivesView, self).get_queryset().filter(
                                    created_time__year=self.kwargs.get('year'),
                                    created_time__month=self.kwargs.get('month')
                                    ).order_by('-created_time')

class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('tag_id'))
        return super(TagView, self).get_queryset().filter(tags=tag).order_by('-created_time')


from django.db.models import Q
def simpleSearch(request):
    error_msg=''
    q = request.GET.get('key')
    if not q:
        error_msg="请输入搜索关键词"
        return render(request,'blog/index.html',context={'error_msg':error_msg})
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})



