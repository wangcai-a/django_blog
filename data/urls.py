from django.urls import path
from . import views

app_name = 'data'

# start with blog
urlpatterns = [
    path('', views.get_week_data, name='data'),
]