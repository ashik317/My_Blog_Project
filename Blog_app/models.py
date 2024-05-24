from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import re

from django.db import models

class Blog(models.Model):
    blog_title = models.CharField(max_length=200)
    blog_content = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    blog_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.blog_title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.blog_title


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-comment_date',]

    def __str__(self):
        return self.comment[:20]

class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="liked_blog")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liker_user")

    def __str__(self):
        return f'{self.user.username} likes {self.blog.blog_title}'
