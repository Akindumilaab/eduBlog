from django.shortcuts import render,redirect,get_object_or_404
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.http import HttpResponseForbidden
from django.contrib import messages
from .decorators import staff_required
from edu_blog.userApp.models import Profile 
from .models import Post, Like, Comment
from .forms import CommentForm
from .models import Post


def home(request):
    posts = Post.objects.filter(approved=True)
    return render(request, 'index.html', {'posts': posts})



# List all posts
def post_list(request):
    category = request.GET.get("category", None)
    
    if category:
        posts = Post.objects.filter(category=category, approved=True)
    else:
        posts = Post.objects.filter(approved=True)
    
    return render(request, "post_list.html", {"posts": posts, "category": category})

# Post Detail View
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        post.approved = True  
        post.save()
        return redirect('home')  

    return render(request, "post_detail.html", {"post": post})


@login_required
@staff_required  
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Assign logged-in user as author
            post.approved = True  # Auto-approve posts (optional)
            post.save()
            messages.success(request, "Blog post created successfully!")
            return redirect('post_list')  # Redirect to the post list
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.approved = True
            post.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
        return render(request, 'Edit_post.html', {'form': form , 'post': post})

        
        
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('post_list')





@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()  # Unlike if already liked
        messages.info(request, "You unliked this post.")
    else:
        messages.success(request, "You liked this post.")

    return redirect('post_detail', post_id=post.id)



@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user  
            comment.save()
            return redirect('post_detail', post_id=post.id)  

    return redirect('post_detail', post_id=post.id)  



def all_likes(request):
    likes = Like.objects.all()
    return render(request, 'all_likes.html', {'likes': likes})

def all_comments(request):
    comments = Comment.objects.all()
    return render(request, 'all_comments.html', {'comments': comments})



def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    messages.success(request, "Comment deleted successfully.")
    return redirect('post_detail', comment.post.id)  


@login_required
def Approve_disapprove_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Only superusers or staff can approve/disapprove posts
    if not request.user.is_superuser and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to approve or disapprove posts.")

    if request.method == "POST":
        post.approved = not post.approved  # Toggle approval status
        post.save()
        
        if post.approved:
            messages.success(request, "Post has been approved.")
        else:
            messages.warning(request, "Post has been disapproved.")

        return redirect("post_detail", post_id=post.id)

    return redirect("post_list")  




