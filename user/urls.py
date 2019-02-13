from django.urls import path
from . import views

app_name = 'user'

# start with blog
urlpatterns = [
    path('register/', views.register, name='register'),
    path('usercenter/', views.user_center, name='usercenter'),
    path('activate/', views.user_activate, name='useractivate')
]