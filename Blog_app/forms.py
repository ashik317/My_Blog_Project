from django import forms
from Blog_app.models import Blog, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)