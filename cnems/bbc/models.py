from django.db import models
import os
import random
from django.utils import timezone
from django.conf import settings
import datetime
from DjangoUeditor.models import UEditorField

PORTRAIT_DEFAULT_PATH = 'bbc/img/1212.jpg'
NEWS_DEFAULT_PATH = 'bbc/img/QQ.jpg'

def user_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1]
    fn = '%s_%s%s' % (timezone.now().strftime('%Y%m%d%H%M%S'),
                      random.randint(100000, 999999), ext)
    return 'portrait/%s' % fn


def news_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1]
    fn = '%s_%s%s' % (timezone.now().strftime('%Y%m%d%H%M%S'),
                      random.randint(100000, 999999), ext)
    return 'news/%s' % fn

# 用户类
class Users(models.Model):
    neck_name = models.CharField(max_length=20,default='')
    phone = models.CharField(max_length=11)
    password = models.CharField(max_length=50)
    number   = models.IntegerField(default=1)
    vip = models.CharField(max_length=1, default=0)
    integral = models.IntegerField(default=0)
    portrait = models.ImageField(upload_to=news_upload_to)

    def get_url(self):
        if self.portrait:
            return self.portrait.url
        else:
            return settings.STATIC_URL + PORTRAIT_DEFAULT_PATH



# 充值记录表
class Pays(models.Model):
    pays_number = models.CharField(max_length=20, unique=True)
    pays_time = models.DateTimeField(default=timezone.now)
    users = models.ForeignKey(Users, on_delete=models.CASCADE)
    pays_money = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.CharField(max_length=5)


#  发布内容表
class News(models.Model):
    CHECK_STATUS = (
        ('0', '正在审核'),
        ('1', '审核通过'),
        ('-1', '审核失败')
    )
    news_title = models.CharField(max_length=50)
    news_sort = models.CharField(max_length=4)
    news_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    news_source = models.CharField(max_length=50)
    news_center = models.CharField(max_length=100)
    news_portrait = models.ImageField(upload_to=news_upload_to)
    news_content = UEditorField('富文本新闻内容', width=600, height=500,
                                toolbars='full',imagePath='',filePath='',
                                upload_settings={'imageMaxSize':1204000},
                                settings={},command=None,blank=True)
    news_check = models.CharField(max_length=2, choices=CHECK_STATUS,default=0)
    news_look = models.IntegerField(default=0)
    news_share = models.IntegerField(default=0)
    news_time = models.DateTimeField(default=timezone.now)
    news_author = models.CharField(max_length=10, default='')
    news_likes = models.IntegerField(default=0)

    def get_news_url(self):
        if self.news_portrait:
            return self.news_portrait.url
        else:
            return settings.STATIC_URL + NEWS_DEFAULT_PATH

    def ago_time(self):
        now_time = timezone.now()
        times = now_time - self.news_time
        print(times)
        if now_time - self.news_time > datetime.timedelta(days=1):
            times = str(times.days) + '天前'
        elif datetime.timedelta(hours=1) < now_time - self.news_time < datetime.timedelta(days=1):
            times = str(times)[:2] + '小时前'
        elif datetime.timedelta(minutes=1) < now_time - self.news_time < datetime.timedelta(hours=1):
            times = str(times)[2:4] + '分钟前'
        else:
            times = '刚刚'

        print(times)
        return times.replace(':', '')


# 积分兑换表
class NumberUser(models.Model):
    # 用户
    user2 = models.ForeignKey(Users, on_delete=models.CASCADE)
    # 时间
    time = models.DateTimeField(default=timezone.now)
    # 交易详情
    pays = models.CharField(max_length=10)
    # 积分
    money = models.DecimalField(max_digits=10, decimal_places=2)


class Likes(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    users = models.ForeignKey(Users, on_delete=models.CASCADE)

class Comments(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    comment_center = models.CharField(max_length=200)
    users = models.ForeignKey(Users, on_delete=models.CASCADE)
    comment_time = models.DateTimeField(default=timezone.now)

    def ago_2_time(self):
        now_time = timezone.now()
        times = now_time - self.comment_time
        print(times)
        if now_time - self.comment_time > datetime.timedelta(days=1):
            times = str(times.days) + '天前'
        elif datetime.timedelta(hours=1) < now_time - self.comment_time < datetime.timedelta(days=1):
            times = str(times)[:2] + '小时前'
        elif datetime.timedelta(minutes=1) < now_time - self.comment_time < datetime.timedelta(hours=1):
            times = str(times)[2:4] + '分钟前'
        else:
            times = '刚刚'

        print(times)
        return times.replace(':', '')