from django.shortcuts import render, redirect
from .forms import RegisterForm

# Create your views here.


def register(request):
    print(request.method)
    # 请求为post的时候,才表示用户提交了数据
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # 验证数据的合法性
        if form.is_valid():
            form.save()
            return redirect('/')
    # 请求不是post表示用户正在访问注册页面,展示一个空的表单给用户
    else:
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问页面,则渲染一个空的表单
    # 如果提交一个不合法的信息,则渲染带有错误信息的表单
    return render(request, 'register.html', context={'form': form})