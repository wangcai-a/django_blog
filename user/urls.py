from django.urls import path, re_path
from . import views

app_name = 'user'

# start with blog
urlpatterns = [
    path('register/', views.register, name='register'),
    path('usercenter/', views.user_center, name='usercenter'),
    re_path(r'^activate/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', views.user_activate, name='activeuser')
]
