from django.shortcuts import render, redirect
from .forms import RegisterForm

# Create your views here.


def register(request):
    # 从get或者post请求中获取next参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    # redirect_to = request.POST.get('next', request.GET.get('next', ''))

    # 请求为post的时候,才表示用户提交了数据
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # 验证数据的合法性
        if form.is_valid():
            form.save()
            return redirect('/user/login/')
    # 请求不是post表示用户正在访问注册页面,展示一个空的表单给用户
    else:
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问页面,则渲染一个空的表单
    # 如果提交一个不合法的信息,则渲染带有错误信息的表单
    return render(request,
                  'register.html',
                  # context={'form': form, 'next':redirect_to}
                  context={'form': form}
                  )