"""bpm_dj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from blog import views

app_name = 'blog'
"""
urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$',views.detail, name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.archives, name='archives'),
    url(r'^get_categories/(?P<category_id>[0-9]+)/$',views.get_categories, name='get_categories'),
]
"""
#http://zmrenwu.com/post/33/
#IndexView 是一个类，不能直接替代 index 函数。好在将类视图转换成函
#数视图非常简单，只需调用类视图的 as_view() 方法即可
urlpatterns = [
    url(r'^index/', views.IndexView.as_view(), name='index'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.ArchivesView.as_view(), name='archives'),
    url(r'^get_categories/(?P<category_id>[0-9]+)/$',views.CategoryView.as_view(), name='get_categories'),
    url(r'^get_tags/(?P<tag_id>[0-9]+)/$',views.TagView.as_view(), name='get_tags'),
    url(r'^post/(?P<pk>[0-9]+)/$',views.detail, name='detail'),
    url(r'^search/', views.simpleSearch, name='search'),
]


