from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('study_tips', 'Study Techniques & Learning Strategies'),
        ('mental_health', 'Mental Health Tips for Students'),
        ('career_guidance', 'Guidance on Career Choices'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='postImages/', null=True)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    




    class Post(models.Model):
        title = models.CharField(max_length=200)
        content = models.TextField()
        author = models.ForeignKey(User, on_delete=models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)

        def total_likes(self):
            return self.likes.count()

        def total_comments(self):
            return self.comments.count()

        def __str__(self):
            return self.title

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ('user', 'post')  # Prevent duplicate likes

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
