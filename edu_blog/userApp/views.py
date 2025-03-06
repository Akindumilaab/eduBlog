from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from .forms import ProfileForm, UserForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import messages
from edu_blog.blogApp.decorators import staff_required


# Create your views here.

class SignUpView(generic.CreateView):
    form_class = SignupForm
    success_url  = reverse_lazy("login")
    template_name = 'registration/signup.html'


@login_required
def ProfileView(request):
    profile = get_object_or_404(Profile, user_id=request.user.id)  # Get the logged-in user's profile
    user = get_object_or_404(User, id=request.user.id)

    if request.method == "POST":
        profileForm = ProfileForm(request.POST, request.FILES, instance=profile)
        userForm = UserForm(request.POST, instance=user)

        if profileForm.is_valid() and userForm.is_valid():
            profileForm.save()
            userForm.save()
            
            return redirect("profile")  # Redirect to profile page after saving

    else:
        profileForm = ProfileForm(instance=profile)
        userForm = UserForm(instance=user)

    return render(request, "profile.html", {"user_form":userForm, "profile_form": profileForm})

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user_id=request.user.id)  # Get the logged-in user's profile
    user = get_object_or_404(User, id=request.user.id)

    if request.method == "POST":
        profileForm = ProfileForm(request.POST, request.FILES, instance=profile)
        userForm = UserForm(request.POST, instance=user)

        if profileForm.is_valid() and userForm.is_valid():
            profileForm.save()
            userForm.save()
            
            return redirect("profile")  # Redirect to profile page after saving

    else:
        profileForm = ProfileForm(instance=profile)
        userForm = UserForm(instance=user)

    return render(request, "edit_profile.html", {"user_form":userForm, "profile_form": profileForm})

@staff_required
@login_required
def view_user_staff(request):
      
        staff_users = User.objects.filter(is_staff=True)
        all_users = User.objects.all()
        return render(request, "view_users.html", {"staff_users": staff_users, "all_users": all_users})
    
        # return render(request, "access_denied.html") 
    
     
@staff_required
@login_required
def makeStaff(request, userId):
    if not request.user.is_superuser:
        messages.error(request, "Only superusers can change staff status.")
        return redirect("view-user", action="staff")

    user = get_object_or_404(User, id=userId)
    if user.is_staff:
        user.is_staff = False
        messages.success(request, "User is no longer a staff member.")
    else:
        user.is_staff = True
        messages.success(request, "User is now a staff member.")

    user.save()
    return redirect("view-user", action="staff")

