from django.urls import path, re_path, register_converter
from . import views, urls_converters
register_converter(urls_converters.FourDigitYearConverter, 'xxx')

app_name = 'polls'
urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<xxx:year>/question/', views.show_year_question, name='vvv'),
    re_path(r'^(?P<year>[0-9]{4})/year_question/$', views.show_year_question, name='111')
]