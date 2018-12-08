from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UsersForm
from django.contrib.auth.models import User
from .models import Users, News
from django.contrib.auth import authenticate,login
from django.urls import reverse
import hashlib
from .dysms_python import demo_sms_send as b
import uuid
from .dysms_python.demo_sms_send import *
from django.views.decorators.csrf import csrf_exempt
import random
#  对密码进行加密
def md5_en(base_password):
    md5 = hashlib.md5()
    md5.update(base_password.encode('utf8'))
    return md5.hexdigest()

def register(request):
    """
    进入注册页面
    :param request:
    :return:
    """
    context = dict()
    form = UsersForm()
    context['form'] = form
    return render(request, 'bbc/register.html',context)

def login_user(request):
    """
    注册信息进行处理，进入登录页面,进行登录
    :param request:
    :return:
    """
    context = dict()
    form = UsersForm()
    if request.method == 'POST':
        form = UsersForm(request.POST)
        if form.is_valid():
            if not Users.objects.filter(phone=request.POST['phone']).exists():
                veri = request.POST['ver']
                if veri == request.session['ver']:
                    password = form.cleaned_data['password']
                    password_t = request.POST['password_t']
                    if password == password_t:
                        password = md5_en(password)
                        Users.objects.create(phone=request.POST['phone'], password=password)
                        context['form'] = form
                        return render(request, 'bbc/page2.html', context)

                    error_message = '两次密码输入不一致'
                    context['error_message'] = error_message
                error_message = '验证码输入错误'
                context['error_message'] = error_message
            error_message = '该手机号已注册过'
            context['error_message'] = error_message
    context['form'] = form
    return render(request, 'bbc/register.html',context)

# 登录进入首页
def login_2(request):
    context = dict()
    form = UsersForm()
    if request.method == 'POST':
        form = UsersForm(request.POST)
        if form.is_valid():
            password_1 = request.POST['password']
            phone = request.POST['phone']
            password = md5_en(password_1)
            user = Users.objects.filter(phone=phone, password=password)
            print(user)
            if not user:
                context['form'] = form
                error_message = '手机号或密码错误！'
                context['error_message'] = error_message
                return render(request, 'bbc/login.html', context)
            request.session['loginuser'] = phone
            if request.POST.get('aa'):
                request.session['phone'] = phone
                request.session['password'] = password_1
            news = News.objects.all()[:3]
            news_1 = news[0]
            news_2 = News.objects.filter(news_sort='快讯')
            news_xw = News.objects.filter(news_sort='新闻')[:4]
            news_zc = News.objects.filter(news_sort='政策')
            news_hq = News.objects.filter(news_sort='行情')
            news_js = News.objects.filter(news_sort='技术')
            return render(request, 'bbc/login_out.html',
                          {'user_1': user[0], 'news_1': news_1, 'news_2': news_2[0],
                           'news_3': news_2[1], 'news_4': news_2[2],'news':news,
                           'news_xw':news_xw,'news_zc':news_zc,'news_hq':news_hq,'news_js':news_js})

    context['form'] = form
    context['phone'] = request.session.get('phone','')
    context['pwd'] = request.session.get('password','')
    return render(request, 'bbc/login.html',context)


# 忘记密码
def find_pwd(request):
    return render(request, 'bbc/update_password.html')

# 验证忘记密码输入的信息
def find_2_pwd(request):
    context = dict()
    if request.method == 'POST':
        phone = request.POST.get('phone', None)
        if phone:
            context['phone'] = phone
            return render(request, 'bbc/set_password.html',context)
        error_message = '请输入正确手机号'
        context['error_message'] = error_message
        return render(request, 'bbc/update_password.html', context)
    return render(request, 'bbc/update_password.html')

# 重置密码后对密码进行加密保存
def find_3_pwd(request,phone):
    context = dict()
    if request.method == 'POST':
        user = Users.objects.get(phone=phone)
        password = request.POST['password']
        password_t = request.POST['password_t']
        if password == password_t:
            password = md5_en(password)
            user.password = password
            user.save()
            return HttpResponseRedirect(reverse('bbc:login_2'))
        error_message = '密码需输入一致'
        context['error_message'] = error_message
        return render(request, 'bbc/set_password.html', context)
    return render(request, 'bbc/update_password.html')

# 个人资料
def set_person(request):
    user = request.session.get('loginuser')
    if user:
        user_1 = Users.objects.get(phone=user)
        news = user_1.news_set.all()
        return render(request, 'bbc/set_person.html',{'user_1':user_1,'news':news})
    return HttpResponseRedirect(reverse('bbc:login_out'))

#  保存个人资料信息
def save_set_person(request):
    user = request.session.get('loginuser')
    if user:
        user_1 = Users.objects.get(phone=user)
        if request.method == 'POST':
            img = request.FILES.get('portrait', None)
            n_name = request.POST.get('neck_name', None)
            if img:
                user_1.portrait = img
                user_1.save()
            if n_name:
                user_1.neck_name = n_name
                user_1.save()
        return render(request, 'bbc/set_person.html', {'user_1':user_1})
    return HttpResponseRedirect(reverse('bbc:login_out'))

#  获取验证码
def change_pwd(request):
    user = request.session.get('loginuser')
    if user:
        user_1 = Users.objects.get(phone=user)
        return render(request, 'bbc/change_pwd.html', {'user_1': user_1})
    return HttpResponseRedirect(reverse('bbc:login_out'))

#  判断验证码，进入密码修改
def change_pwd_2(request):
    user = request.session.get('loginuser')
    if user:
        user_1 = Users.objects.get(phone=user)
        if request.method == 'POST':
            num = request.POST.get('ver')
            if num:
                if num == request.session.get('ver'):
                    return render(request, 'bbc/change_pwd_2.html',{'user_1':user_1})
                message = '验证码错误'
                return render(request, 'bbc/change_pwd.html', {'user_1': user_1,'message':message})
            else:
                message = '请先获取验证码'
                return render(request, 'bbc/change_pwd.html', {'user_1': user_1, 'message': message})
        return render(request, 'bbc/change_pwd.html', {'user_1':user_1})
    return HttpResponseRedirect(reverse('bbc:login_out'))

#  修改密码后进行保存
def save_pwd(request):
    context = dict()
    user = request.session.get('loginuser')
    if user:
        user_1 = Users.objects.get(phone=user)
        if request.method == 'POST':
            new_pwd = request.POST['new_pwd']
            new_pwd_2 = request.POST['new_pwd_2']
            if new_pwd == new_pwd_2:
                new_pwd = md5_en(new_pwd)
                user_1.password = new_pwd
                user_1.save()
                message = '密码修改成功！'
                context['message'] = message
            message = '密码输入不一致'
            context['message'] = message
        context['user_1'] = user_1
        return render(request, 'bbc/change_pwd_2.html', context)
    return HttpResponseRedirect(reverse('bbc:login_out'))

# 退出登录
def login_out(request):
    user = request.session.get('loginuser')
    news = News.objects.all()[:3]
    news_1 = news[0]
    news_2 = News.objects.filter(news_sort='快讯')
    news_xw = News.objects.filter(news_sort='新闻')[:4]
    news_zc = News.objects.filter(news_sort='政策')
    news_hq = News.objects.filter(news_sort='行情')
    news_js = News.objects.filter(news_sort='技术')
    if user:
        request.session.pop('loginuser')
    return render(request, 'bbc/login_out.html', {'news':news,'news_1':news_1,'news_2':news_2[0],
                                                  'news_3':news_2[1],'news_4':news_2[2],'news_xw':news_xw,
                                                  'news_zc':news_zc,'news_hq':news_hq,'news_js':news_js})


#  登录后返回首页
def face(request):
    user = request.session.get('loginuser')
    if user:
        user_1 = Users.objects.get(phone=user)
        news = News.objects.all()[:3]
        news_1 = news[0]
        news_2 = News.objects.filter(news_sort='快讯')
        news_xw = News.objects.filter(news_sort='新闻')
        news_zc = News.objects.filter(news_sort='政策')
        news_hq = News.objects.filter(news_sort='行情')
        news_js = News.objects.filter(news_sort='技术')
        return render(request, 'bbc/login_out.html', {'user_1':user_1,'news':news,'news_1':news_1,'news_2':news_2[0],
                                                      'news_3':news_2[1], 'news_4':news_2[2],'news_xw':news_xw,'news_zc':news_zc,
                                                      'news_hq':news_hq, 'news_js':news_js})
    return HttpResponseRedirect(reverse('bbc:login_out'))

@csrf_exempt
def verify(request):
    __business_id = uuid.uuid1()
    number = random.randint(100000, 999999)
    params = dict(code=str(number))
    request.session['ver']= params['code']
    request.session.set_expiry(120)
    send_result = send_sms(__business_id, request.POST['phone'], "既念即觉一生一重", "SMS_151578730", params)
    return HttpResponse('ok')

