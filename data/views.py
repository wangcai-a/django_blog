from django.shortcuts import render

# Create your views here.


def site_data(request):
    return render(request, 'data.html')
