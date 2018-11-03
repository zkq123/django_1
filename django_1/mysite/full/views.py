from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseNotModified,HttpResponseBadRequest
from django.utils import timezone
from django.http import HttpResponseForbidden,  HttpResponseNotAllowed,HttpResponseGone, JsonResponse
from django.http import StreamingHttpResponse,FileResponse
from django.conf import settings
from django.urls import reverse
from django.http import StreamingHttpResponse
import datetime
import json
import os
import random
import csv
def default_index(request):
    response = HttpResponse('this girl seems sad')
    print(response.content)
    response.write('<br/>')
    response.write('<h1>Do not be sad</h1>')
    print(response.charset)  # utf8
    response.status_code = 404
    print(response.reason_phrase)   # 200
    response.status_code = 200
    print(response.reason_phrase)
    print(response.closed)
    response = HttpResponse('国不破，山河犹在',content_type='text/html',status=220, reason='ok',charset='gb2312' )
    print(response.status_code)
    print(response.reason_phrase)
    response['girl_name'] = 'alice'
    response.__setitem__('girl_sex', 'girl')

    response.__delitem__('girl_sex')
    print('response.__getitem__=', response.__getitem__('girl_name'))
    if response.has_header("this has header"):
        print("this header is not exists")
    elif response.has_header('girl_name'):
        print("response['girl_name']=", response['girl_name'])
    else:
        print("no no no no n o")
    response.setdefault('girl_sex', 'girl')
    response.set_cookie('login_user', 'zkq111',max_age=20,
                        expires=timezone.now() + datetime.timedelta(days=1))
    response.set_cookie('login_user_2', 'zkq222',
                        expires=timezone.now() + datetime.timedelta(days=1))

    request.session['user_login'] = 'zzkkqq'
    print(request.session['user_login'])
    print(request.COOKIES.get('sessionid'))
    print(request.COOKIES)
    return response

def download_file(request, file_type):
    if file_type == 1:
        file_content = 'shjcicsaciud'
        response = HttpResponse(file_content, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment;filename="1.txt"'
        return response
    else:
        return HttpResponse('未处理的文件类型')

def write_value(request):
    # response = HttpResponseGone('user_2')
    # return response
    # response = HttpResponseNotAllowed(['GET', 'POST'])
    # return response
    # response = HttpResponseForbidden("sdfdsf")
    # return response
    # response = HttpResponseBadRequest('cfsdgbvfds')
    # return response
    # response = HttpResponseRedirect('http://127.0.0.1:8000/read/')
    # return response
    # response = HttpResponseNotModified()
    # response = HttpResponse()
    # response.set_signed_cookie('user_2',123,salt=settings.SIGNED_COOKIES_SALT,path='/')
    # response.write('<br />read cookie user_buy_count with salt=' +
    #                request.get_signed_cookie('user_2',
    #                                          salt=settings.SIGNED_COOKIES_SALT))
    # list_9 = [1323,'这','dwd','43fec']
    # response.writelines(list_9)
    # response.write('<br>user_2')
    d = dict(a=1, b='我', c=['a', 'b', 'd'])
    c = ['a', 'b', 'd']
    response = JsonResponse(d,safe=False)
    return response

def read_value(request):
    content = 'username' + request.get_signed_cookie('user_2',
                                                     salt=settings.SIGNED_COOKIES_SALT)
    response = HttpResponse(content)
    return response

def download_img(request):
    file_path = os.path.join(settings.BASE_DIR,'full/static/full/images/11.jpg')
    file_obj = open(file_path, 'rb')
    response = FileResponse(file_obj, as_attachment=False, filename='1212.jpg')
    return response

def first(request):
    print(settings.BASE_DIR)
    return HttpResponse('this is full')


def upload_file(file_obj, ext):
    now = timezone.now()
    filename = '%s%s%s%s%s%s%s%s%s'% (
        now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond,
        random.randint(10000,99999), ext)
    file_path = os.path.join(settings.USER_UPLOAD_DIR, filename)
    with open(file_path,'wb+')as f:
        for chunk in file_obj.chunks():
            print('===================')
            f.write(chunk)

def user_upload_file(request):
    if request.method == 'POST':
        files = request.FILES
        if len(files) == 0:
            return HttpResponseRedirect(reverse('full:upload_fail'))
        for file_key in files:
            print(file_key)         #   up_file
            print('=============')
            file_obj = files[file_key]
            ext = os.path.splitext(file_obj.name)[1]
            upload_file(file_obj,ext)

        return HttpResponseRedirect(reverse('full:upload_success'))
    return render(request, 'full/upload.html')

def upload_success(request):
    return render(request, 'full/upload_success.html')

def upload_fail(request):
    return render(request, 'full/upload_fail.html')

def make_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="somefilename.csv"'
    writer = csv.writer(response)
    # rows = [["Row {} , name=fffffsdfd, age=332, sss".format(idx),
    #          str(idx)]
    #         for idx in range(1065536)]
    # writer.writerow(rows)
    writer.writerow(['First row', 'Foo', 'sbhjc', "'show me the csv'"])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote",dict(a=1,b=2,c=3)])
    return response


class Echo:
    def write(self, value):
        return value

def some_streaming_csv_view(request):
    # 列表生成式外层不使用中括号。而使用小括号。则返回的类型为generator
    rows = (["Row {} , name=fffffsdfd, age=332, sss".format(idx),
             str(idx)]
            for idx in range(1065536))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse(
        (writer.writerow(row) for row in rows),
        content_type="text/csv")
    response['Content-Disposition'] = 'attachment;filename="somefilename2.csv"'
    return response
