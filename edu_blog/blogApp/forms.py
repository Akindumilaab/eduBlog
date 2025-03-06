
from django import forms
from .models import Post
from .models import Comment
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =[
            'title',
            'content',
            'category', 
            'image'
        ]



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']  # Ensure your Comment model has a 'text' field
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment...'}),
        }