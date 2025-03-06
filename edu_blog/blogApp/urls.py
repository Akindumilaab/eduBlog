from django.urls import path
from .views import *


urlpatterns = [
    path("posts", post_list, name="post_list"),  # Show all posts
    path("<int:post_id>/", post_detail, name="post_detail"),  # Post details
    path("create-post/", create_post, name="create-post"),
    path('edit-post/<int:post_id>/', edit_post, name="edit-post"),
    path('delete-post/<int:post_id>/', delete_post, name="delete-post"),
    path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('all-likes/', all_likes, name='all-likes'),
    path('all-comments/', all_comments, name='all-comments'),
    path('delete-comment/<int:comment_id>/', delete_comment, name='delete-comment'),
    path("post/<int:post_id>/Approve-disapprove-post/", Approve_disapprove_post, name="Approve-disapprove-post"),
]


