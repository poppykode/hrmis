from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('',views.login, name='login'),
    path('redirect',views.redirect_logged,name='redirect_logged'),
    path('admin-dash',views.admin_dash,name='admin_dash'),
    path('employee-dash',views.employee_dash,name='employee_dash'),
    path('sign-up',views.sign_up,name='sign_up'),
    path('users',views.users, name='users'),
    path('users/<str:filter>',views.users, name='users'),
    path('toggle-user-status/<int:pk>',views.toggle_user_status, name='toggle_user_status'),
    path('edit-profile-admin/<int:pk>',views.edit_profile_admin, name='edit_profile_admin'),
    path('profile/<int:pk>',views.profile, name='profile'),
    path('change-password/<int:pk>',views.change_password, name='change_password'),
    
]
