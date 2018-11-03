from django.urls import path
from . import views as mysite_views
app_name = 'full'
urlpatterns = [
    path('',mysite_views.default_index, name='default_index'),
    path('download/<int:file_type>/', mysite_views.download_file, name='download_file'),
    path('write/', mysite_views.write_value, name='write_va lue'),
    path('read/', mysite_views.read_value, name='read_value'),
    path('download_img/', mysite_views.download_img),
    path('first/', mysite_views.first, name='first'),
    path('upload_file/', mysite_views.user_upload_file, name='user_upload_file'),
    path('upload_success/', mysite_views.upload_success, name='upload_success'),
    path('upload_fail/', mysite_views.upload_file, name='upload_fail'),
    path('make_csv', mysite_views.make_csv),
    path('make2_csv', mysite_views.some_streaming_csv_view)
]