from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User
from .models import User_ex
from django import forms


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(label='用户邮箱', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'placeholder': '请输入您注册时的邮箱',
    }))
    pwd_1 = forms.CharField(label='新密码', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'pwd_1',
        'placeholder': '请输入新密码'
    }))
    pwd_2 = forms.CharField(label='重复密码', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'pwd_2',
        'placeholder': '请再输入一次密码'
    }))
    check_code = forms.CharField(label='验证码', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'check_code',
        'placeholder': '请输入验证码'
    }))

    # 验证邮箱是否存在
    def clean_email(self):
        email = self.cleaned_data.get('email')
        users = User.objects.filter(email=email)

        if users.count() == 0:
            raise ValidationError('该邮箱没有被注册,请重新填写')
        return email

    # 验证两次输入密码是否一致
    def clean_pwd_2(self):
        pwd_1 = self.cleaned_data.get('pwd_1')
        pwd_2 = self.cleaned_data.get('pwd_2')

        if pwd_1 != pwd_2:
            raise ValidationError('两次密码不一致,请重新填写')
        return pwd_2

    # 检测验证码是否正确
    def clean_check_code(self):
        try:
            # 获取对应的用户
            email = self.cleaned_data.get('email')
            check_code = self.cleaned_data.get('check_code')
            user = User.objects.filter(email=email)

            # 回去用户对应的信息
            user_ex = User_ex.objects.filter(user=user)
            if user_ex.count() > 0:
                raise ValidationError('未获取验证码')
            if user_ex.valid_code != check_code:
                raise ValidationError('验证码不正确')
        except Exception as e:
            return ValidationError('验证码不对或失效')





