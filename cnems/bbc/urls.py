from django.urls import path
from . import views, other_views
app_name = 'bbc'

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login_user, name='login_user'),
    path('login_2', views.login_2, name='login_2'),
    path('find_pwd', views.find_pwd, name='find_pwd'),
    path('find_2_pwd', views.find_2_pwd, name='find_2_pwd'),
    path('find_3_pwd/<int:phone>', views.find_3_pwd, name='find_3_pwd'),
    path('set_person', views.set_person, name='set_person'),
    path('change_pwd', views.change_pwd, name='change_pwd'),
    path('change_pwd_2', views.change_pwd_2, name='change_pwd_2'),
    path('', views.login_out, name='login_out'),
    path('save_set_person', views.save_set_person, name='save_set_person'),
    path('save_pwd', views.save_pwd, name='save_pwd'),
    path('face', views.face, name='face'),
    path('verify', views.verify, name='verify'),

   ]
# other_views
urlpatterns += [
    path('my_vip', other_views.my_vip, name='my_vip'),
    path('my_integral', other_views.my_integral, name='my_integral'),
    path('my_news', other_views.my_news, name='my_news'),
    path('publish_comment', other_views.publish_comment, name='publish_comment'),
    path('pay', other_views.pay, name='pay'),
    path('pay_2', other_views.pay_2, name='pay_2'),
    path('exchange', other_views.exchange, name='exchange'),
    path('exchange_2', other_views.exchange_2, name='exchange_2'),
    path('publish_save', other_views.publish_save, name='publish_save'),
    path('my_publish', other_views.my_publish, name='my_publish'),
    path('publish_success', other_views.publish_success, name='publish_success'),
    path('<int:news_id>/news_comment', other_views.news_comment, name='news_comment'),
    path('<int:news_id>/news_likes', other_views.news_likes, name='news_likes'),
    path('<int:news_id>/kx_comment', other_views.kx_comment, name='kx_comment'),
    path('kx', other_views.kx, name='kx'),
    path('<int:news_id>/comment', other_views.comment, name='comment'),
    path('news_list', other_views.news_list, name='news_list')
]