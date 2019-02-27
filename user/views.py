from django.shortcuts import render, redirect
from .forms import RegisterForm, ForgetPasswordForm, EmailCodeForm
from .models import User, User_ex
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password

# Create your views here.
from itsdangerous import URLSafeTimedSerializer as utsr
import base64
import random, string
import re
from django.conf import settings as django_settings
from django.core.mail import send_mail
from django.utils import timezone


class Token:
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.encodebytes(bytes(security_key, encoding="utf8"))

    def generate_validate_token(self, username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)

    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)

    def remove_validate_token(self, token):
        serializer = utsr(self.security_key)
        print(serializer.loads(token, salt=self.salt))
        return serializer.loads(token, salt=self.salt)


token_confirm = Token(django_settings.SECRET_KEY)    # 定义为全局变量


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
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2')
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
            user.save()
            token = token_confirm.generate_validate_token(username)
            message = "\n".join([u'{0},欢迎加入我的博客'.format(username), u'请访问该链接，完成用户验证:',
                                 '/'.join([django_settings.DOMAIN, 'user/activate', token])])
            send_mail(u'注册用户验证信息', message, '535719197@qq.com', [email], fail_silently=False)
            return render(request, 'message.html', {'message': u"请登录到注册邮箱中验证用户，有效期为1个小时"})
            return redirect('/user/login/')
    # 请求不是post表示用户正在访问注册页面,展示一个空的表单给用户
    else:
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问页面,则渲染一个空的表单
    # 如果提交一个不合法的信息,则渲染带有错误信息的表单
    return render(request,
                  'registration/register.html',
                  # context={'form': form, 'next':redirect_to}
                  context={'form': form}
                  )


def user_center(request):
    return render(request, 'user_center.html')


def user_activate(request, token):
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        username = token_confirm.remove_validate_token(token)
        users = User.objects.filter(username=username)
        for user in users:
            user.delete()
        return render(request, 'message.html', {'message': "对不起,验证码已经过期,请重新注册",})
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'message.html', {'message': "对不起,用户不存在,请重新注册"})
    user.is_active = 1
    user.save()
    message = '验证成功,请登录'
    return render(request, 'message.html', {'message': message})


def forget_password(request):
    data = {}
    data['form_title'] = '重置密码'
    data['submit_name'] = '重置密码'

    if request.method == 'POST':
        # 表单提交
        form = ForgetPasswordForm(request.POST)

        # 验证是否合法
        if form.is_valid():
            email = form.cleaned_data['email']
            pwd = form.cleaned_data['pwd_2']
            username = form.cleaned_data['username']
            check_code = form.cleaned_data['check_code']
            user = User.objects.get(email=email, username=username)
            user.set_password(pwd)
            user.save()

            # 删除验证码
            ex = User_ex.objects.filter(vaild_code=check_code)
            if ex.count() > 0:
                ex.delete()

            # 重新登录
            user = authenticate(username=user.username, password=pwd)
            if user is not None:
                login(request, user)

            # 页面提示
            data['goto_url'] = reversed('user_info')
            data['goto_time'] = 3000
            data['goto_page'] = True
            data['message'] = '修改密码成功'
            return render(request, 'message.html', data)
    else:
        form = ForgetPasswordForm()
    data['form'] = form
    return render(request, 'password_reset_form.html', data)


def get_email_code(request):
    data = {}
    data['form_title'] = '重置密码'
    data['submit_name'] = '获取验证码'

    if request.method == 'POST':
        # 表单提交
        form = EmailCodeForm(request.POST)

        # 验证是否合法
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            # string.digits生成0-9数字字符串, string.ascii_letters生成a-Z所有字母的字符串
            # 随机获取六位数的验证码
            code = ''.join(random.sample(string.digits + string.ascii_letters, 6))
            # 检测短时间内是否生成过验证码
            users = User.objects.filter(email=email, username=username)
            user_ex = User_ex.objects.filter(user_id=users[0].id)
            if user_ex.count() > 0:
                user_ex = user_ex[0]

                create_time = user_ex.vaild_time
                td = timezone.now() - create_time
                if td.seconds < 60:
                    data['message'] = '一分钟之内重复获取验证码'
                    raise Exception(data['message'])
            else:
                # 没有验证码则新建一个
                user_ex = User_ex(user=users[0])
                # 将生成的code写入数据库
                user_ex.vaild_code = code
                user_ex.vaild_time = timezone.now()
                user_ex.save()

                message = "\n".join([u'{0},修改密码的验证码为{1}'.format(username, code)])
                send_mail(u'修改密码验证码', message, '535719197@qq.com', [email], fail_silently=False)
                return render(request, 'message.html', {'message': u"请登录到注册邮箱中查看验证码，有效期为1个小时"})

            # 页面提示
            data['goto_url'] = reversed('user_info')
            data['goto_time'] = 3000
            data['goto_page'] = True
            data['message'] = '获取验证码成功'
            return render(request, 'message.html', data)
    else:
        form = EmailCodeForm()
    data['form'] = form
    return render(request, 'send_email.html', data)