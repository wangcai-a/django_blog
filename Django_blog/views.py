from django.shortcuts import render


def home(request):
    # 这里必须使用render不能用render_to_response,否则不能在模板中使用request的属性,比如session等
    return render(request, 'home.html')