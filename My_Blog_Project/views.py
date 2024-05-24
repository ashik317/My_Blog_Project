from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import HttpResponseRedirect, render


def Index(request):
    return HttpResponseRedirect(reverse('Blog_app:blog_list'))

