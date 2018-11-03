from django.urls import path
from . import views
app_name = 'forum'
urlpatterns = [
    path('', views.question_list, name='ppp'),
    path('question_list_2/', views.question_list_2, name='ooo'),
    path('index', views.index, name='index'),
    path('<int:page_1>/page', views.page, name='page'),
    path('<int:page_1>/page_before', views.page_before, name='page_before'),
    path('<int:page_1>/page_dump', views.page_dump, name='page_dump'),

]