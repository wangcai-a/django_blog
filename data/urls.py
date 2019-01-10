from django.urls import path
from . import views

app_name = 'data'

# start with blog
urlpatterns = [
    path('', views.site_data, name='data'),
]