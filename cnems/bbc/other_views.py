from django.shortcuts import render
from .models import Users, Pays, NumberUser, News, Likes, Comments
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
import time
import math
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# 我的会员
def my_vip(request):
    user = request.session.get('loginuser')
    if user:
        user_1 = Users.objects.get(phone=user)
        a = Pays.objects.filter(users=user_1)
        paginator = Paginator(a, 5, 2)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'bbc/my_vip.html', {'user_1':user_1,'a':a, 'cus_list':contacts})
    return HttpResponseRedirect(reverse('bbc:login_out'))

# 我的积分
def my_integral(request):
    user = request.session.get('loginuser')
    if user:
        user_1 = Users.objects.get(phone=user)
        a = NumberUser.objects.filter(user2=user_1)

        paginator = Paginator(a, 5, 2)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'bbc/my_integral.html', {'user_1':user_1,'a':a, 'cus_list':contacts})
    return HttpResponseRedirect(reverse('bbc:login_out'))

# 消息通知
def my_news(request):
    user = request.session.get('loginuser')
    if user:
        user_1 = Users.objects.get(phone=user)
        news = News.objects.all()
        news_1 = user_1.news_set.all()
        list_1 = []
        for i in news_1:
            news_pl = Comments.objects.filter(news=i)
            if news_pl:
                list_1.append(news_pl)
            list_1 = list_1
        print(list_1)
        return render(request, 'bbc/my_news.html', {'user_1': user_1, 'news_pl': list_1,'news':news})
    return HttpResponseRedirect(reverse('bbc:login_out'))


#  新闻发布
def publish_comment(request):
    user = request.session.get('loginuser')
    context = dict()
    if user:
        user_1 = Users.objects.get(phone=user)
        if user_1.number <= 0:
            message = '请先充值发布次数'
            context['message'] = message
            return render(request, 'bbc/login_out.html', context)
        context['user_1'] = user_1
        return render(request, 'bbc/publish_comment.html', context)
    context['message'] = '登录后可进行发布'
    return HttpResponseRedirect(reverse('bbc:login_out'))

# 支付，会员充值
def pay(request):
    user = request.session.get('loginuser')
    if user:

        user_1 = Users.objects.get(phone=user)
        return render(request, 'bbc/pay.html', {'user_1': user_1})
    return HttpResponseRedirect(reverse('bbc:login_out'))


#  会员信息进行修改保存
def pay_2(request):
    user = request.session.get('loginuser')
    if user:
        user_1 = Users.objects.get(phone=user)
        if request.method == 'POST':
            v = request.POST['price']
            m = request.POST['moy']
            m = int(m)
            x = user_1.number
            if v == '1':
                x = x + 2
            if v == '2':
                x = x + 5
            if v == '3':
                x = x + 10
            user_1.number = x
            user_1.save()
            p = request.POST.get('payment', None)
            if not p:
                message = '请选择支付方式'
                return render(request, 'bbc/pay.html',{'user_1': user_1,'message':message})
            number = str(math.ceil(time.time())) + str(random.randint(10000, 99999))
            Pays.objects.create(pays_number=number,users=user_1,pays_money=m,payment=p)
            user_1.number = x
            user_1.save()
            if user_1.vip >= v:
                return HttpResponseRedirect(reverse('bbc:my_vip'))
            user_1.vip = v
            user_1.save()
            return render(request, 'bbc/pay.html', {'user_1':user_1})
        return render(request, 'bbc/pay.html', {'user_1':user_1})
    return HttpResponseRedirect(reverse('bbc:login_out'))

# 积分兑换
def exchange(request):
    user = request.session.get('loginuser')
    if user:
        user_1 = Users.objects.get(phone=user)
        return render(request, 'bbc/exchange.html',{'user_1':user_1})
    return HttpResponseRedirect(reverse('bbc:login_out'))

#  积分兑换进行修改
def exchange_2(request):
    user = request.session.get('loginuser')
    if user:
        user_1 = Users.objects.get(phone=user)
        if request.method == 'POST':
            g = request.POST['intg']
            publish_num = request.POST['price']
            if publish_num == '1':
                user_1.number += 2
            elif publish_num == '2':
                user_1.number += 5
            else:
                user_1.number += 10
            print(publish_num)
            print('=====')
            print(g)
            NumberUser.objects.create(user2=user_1, pays='积分兑换', money=-int(g))
            j = user_1.integral
            user_1.integral = j - int(g)
            user_1.save()
            return HttpResponseRedirect(reverse('bbc:my_integral'))
        return render(request, 'bbc/exchange.html',{'user_1':user_1})
    return HttpResponseRedirect(reverse('bbc:login_out'))

#    新闻保存
def publish_save(request):
    user = request.session.get('loginuser')
    if user:
        user_1 = Users.objects.get(phone=user)
        if request.method == 'POST':
            print('xxxxxxxxxxxxxxxxxxx')
            print(request.POST)
            title = request.POST['comment']
            choice = request.POST['choice']
            author = request.POST['author']
            source = request.POST['source']
            center = request.POST['center']
            face = request.FILES['face']
            comment = request.POST['content']
            News.objects.create(news_title=title,news_sort=choice,
                                news_user=user_1,news_source=source,
                                news_portrait=face,news_content=comment,
                                news_center=center,news_author=author)

        return HttpResponseRedirect(reverse('bbc:publish_success'))
    return HttpResponseRedirect(reverse('bbc:login_out'))


# 我的发布
def my_publish(request):
    user = request.session.get('loginuser')
    if user:
        user_1 = Users.objects.get(phone=user)
        news = user_1.news_set.all()
        return render(request, 'bbc/my_publish.html',{'user_1':user_1,'news':news})
    return HttpResponseRedirect(reverse('bbc:login_out'))


#  发布成功
def publish_success(request):
    user = request.session.get('loginuser')
    if user:
        user_1 = Users.objects.get(phone=user)
        numb = NumberUser.objects.create(user2=user_1,pays='发布文章',money=+100)
        user_1.integral += 100
        user_1.number -= 1
        if user_1.number < 0:
            user_1.number = 0
        user_1.save()
        return render(request, 'bbc/publish_success.html',{'user_1':user_1})
    return HttpResponseRedirect(reverse('bbc:login_out'))


#  新闻详情
def news_comment(request, news_id):
    user = request.session.get('loginuser')

    news = News.objects.all()
    news = news[:5]
    news_1 = News.objects.get(id=news_id)
    news_1.news_look += 1
    news_1.save()
    news_1 = news_1
    return render(request, 'bbc/news_comment.html', {'news':news,'news_1':news_1})



#  点赞
def news_likes(request, news_id):
    user = request.session.get('loginuser')
    if user:
        user_1 = Users.objects.get(phone=user)
        news_1 = News.objects.get(id=news_id)
        a = Likes.objects.filter(users=user_1,news=news_1)
        news = News.objects.all()[:3]
        if a:
            print(news_1.news_likes)
            return render(request, 'bbc/news_comment.html',{'user_1':user_1, 'news_1':news_1,'news':news})
        Likes.objects.create(news=news_1, users=user_1)
        news_1.news_likes += 1
        news_1.save()

        return render(request, 'bbc/news_comment.html',{'user_1':user_1,'news_1':news_1,'news':news})
    return HttpResponseRedirect(reverse('bbc:login_out'))


# 快讯详情
def kx_comment(request, news_id):
    user = request.session.get('loginuser')
    if user:
        user_1 = Users.objects.get(phone=user)
        news = News.objects.all()
        news = news[:5]
        news_1 = News.objects.get(id=news_id)
        news_1.news_look += 1
        news_1.save()
        return render(request, 'bbc/kx_comment.html',{'user_1':user_1,'news':news,'news_1':news_1})
    return HttpResponseRedirect(reverse('bbc:login_out'))

# 快讯列表
def kx(request):
    news_1 = News.objects.filter(news_sort='快讯')
    news  = News.objects.all()[:5]
    user = request.session.get('loginuser')
    if user:
        user_1 = Users.objects.get(phone=user)
        return render(request, 'bbc/kx.html', {'news': news, 'news_1': news_1,'user_1':user_1})
    return render(request, 'bbc/kx.html',{'news':news,'news_1':news_1})



# 发布内容的保存
def comment(request, news_id):
    user = request.session.get('loginuser')
    news_1 = News.objects.get(id=news_id)
    news = News.objects.all()
    news = news[:5]
    if user:
        user_1 = Users.objects.get(phone=user)
        if request.method == 'POST':
            nr = request.POST['py']
            Comments.objects.create(news=news_1,comment_center=nr,users=user_1)
            message = '发布成功'
            return render(request, 'bbc/news_comment.html',{'news':news, 'news_1':news_1,'message':message,'user_1':user_1})
        message = '发布失败'
        return render(request, 'bbc/news_comment.html', {'news':news, 'news_1': news_1, 'message': message,'user_1':user_1})
    return HttpResponseRedirect(reverse('bbc:login_out'))


#  新闻列表
def news_list(request):
    news_1 = News.objects.filter(news_sort='新闻')
    news  = News.objects.all()[:5]
    user = request.session.get('loginuser')
    if user:
        user_1 = Users.objects.get(phone=user)
        return render(request, 'bbc/news_list.html', {'news': news, 'news_1': news_1,'user_1':user_1})
    return render(request, 'bbc/news_list.html',{'news':news,'news_1':news_1})


