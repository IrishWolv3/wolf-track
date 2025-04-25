from django.urls import path
from . import views
from .views import group_list, group_create, group_detail, join_group, leave_group
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name='index'),            ############# Frontend Paths ###############
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'), ############# Authentication Paths ###############
    path('logout/', LogoutView.as_view(next_page='logged_out'), name='logout'),
    path('logged-out/', TemplateView.as_view(template_name='logout.html'), name='logged_out'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('log-workout/', views.log_workout, name='log_workout'), ############# Workout Paths ###############
    path('log-meal/', views.log_meal, name='log_meal'),
    path('groups/', group_list, name='group_list'), #################### Group views ###############
    path('groups/main/', views.group_main, name='group_main'),
    path('groups/create/', group_create, name='group_create'),
    path('groups/<int:group_id>/', group_detail, name='group_detail'),
    path('groups/<int:group_id>/join/', join_group, name='join_group'),
    path('groups/<int:group_id>/leave/', leave_group, name='leave_group'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('conservation/', views.conservation_view, name='conservation'),
]