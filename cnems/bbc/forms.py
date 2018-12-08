from .models import Users
from django import forms
import re
#   注册的表单,登录的表单

def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    value = str(value)
    if not mobile_re.match(value):
        raise forms.ValidationError('手机号码格式错误')

error_dict = dict(required='请输入手机号', max_length='手机号需填11位',min_length='手机号需填11位')
error_dict_2 = dict(required='请输入密码')
class UsersForm(forms.Form):
    phone = forms.CharField(max_length=11,min_length=11,label='手机号',
                            required=True, error_messages=error_dict,

                            )
    password = forms.CharField(max_length=50,required=True,label='密码',
                               widget=forms.PasswordInput(),error_messages=error_dict_2)
