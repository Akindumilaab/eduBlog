from .views import *
from django.urls import path


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView, name='profile'),
    path('edit-profile/', edit_profile, name='edit-profile'),
    path('view-users', view_user_staff, name='view-users'),
    path('make-staff/<int:id>', makeStaff, name='make-staff'),


]