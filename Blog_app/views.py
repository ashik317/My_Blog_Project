from django.forms import BaseModelForm
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DateDetailView, View, TemplateView, DayArchiveView
from Blog_app.models import Blog, Comment, Like
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
from Blog_app.forms import CommentForm


class MyBlogs(LoginRequiredMixin, TemplateView):
    template_name = 'Blog_app/my_blogs.html'

# Create your views here.
def blog_list(request):
    return render(request, 'Blog_app/blog_list.html', context={})


class CreateBlog(LoginRequiredMixin ,CreateView):
    model = Blog
    template_name = 'Blog_app/create_blog.html'
    fields = ('blog_title', 'blog_content', 'blog_image',)

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        title = blog_obj.blog_title
        blog_obj.slug = title.replace(" ", "-") + "-" + str(uuid.uuid4())
        blog_obj.save()
        return HttpResponseRedirect(reverse('index'))
    
class BlogList(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'Blog-app/blog_list.html'

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Blog, Like
from .forms import CommentForm

@login_required
def blog_details(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    already_liked = Like.objects.filter(blog=blog, user=request.user).exists()
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('Blog_app:blog_details', kwargs={'slug': slug}))
    else:
        comment_form = CommentForm()
    
    return render(request, 'Blog_app/blog_details.html', {
        'blog': blog,
        'comment_form': comment_form,
        'already_liked': already_liked,
    })



@login_required 
def Liked(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    user = request.user
    already_liked = Like.objects.filter(blog=blog, user=user).exists()
    if not already_liked:
        like_post = Like(user=user, blog=blog)
        like_post.save()
    return HttpResponseRedirect(reverse('Blog_app:blog_details', kwargs={'slug': blog.slug}))


@login_required
def Unliked(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    user = request.user
    already_liked = Like.objects.filter(blog=blog, user=user)
    if already_liked.exists():
        already_liked.delete()
    return HttpResponseRedirect(reverse('Blog_app:blog_details', kwargs={'slug': blog.slug}))

