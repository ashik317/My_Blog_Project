from django.urls import path, re_path
from Blog_app import views

app_name = 'Blog_app'

urlpatterns = [
    path('', views.BlogList.as_view(), name='blog_list'),
    path('write/', views.CreateBlog.as_view(), name='create_blog'),
    re_path(r'details/(?P<slug>[-a-zA-Z0-9_?]+)/$', views.blog_details, name='blog_details'),
    path('like/<int:pk>/', views.Liked, name='liked_post'),
    path('unlike/<int:pk>/', views.Unliked, name='unliked_post'),
     path('my_blog/', views.MyBlogs.as_view(), name='my_blogs'),
]
