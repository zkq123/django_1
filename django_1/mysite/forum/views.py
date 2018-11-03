from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from . models import Blog
from django.http import HttpResponse
import json
from django.http import Http404
from . models import Author
from django.views.decorators.http import require_http_methods
import math
def question_list(request):
    datas = [dict(id=o.id, name=o.name,create_time=o.create_time.strftime('%Y-%m-%d %H:%M:%S'))for o in Blog.objects.filter(create_time__year=2018)]
    if len(datas) == 0:
        raise Http404("你这没信息呀")
    else:
        result = json.dumps(datas)
        response = HttpResponse(result)
        print(request.path)
        return redirect('forum:ooo')



def question_list_2(request):
    datas = [dict(id=o.id, name=o.name,create_time=o.create_time.strftime('%Y-%m-%d %H:%M:%S'))for o in Blog.objects.all()]

    print(request.path_info)
    if request.method == 'GET':
        if len(datas) == 0:
            raise Http404("你这没信息呀")
        else:
            result = json.dumps(datas)
            return HttpResponse(result)
    elif request.method == 'POST':
        print(request.method)



def index(request):
    b = get_list_or_404(Blog, id__gt=1)
    return HttpResponse(b)

page_1 = 1
def page(request, page_1):
    a = Author.objects.all()
    data_count = len(a)
    page_count = int(data_count/2)
    if data_count % 2 > 0:
        page_count += 1
    show_list = a[2 * (page_1 - 1): 2 * page_1]
    page_1 += 1
    if page_1 > page_count:
        page_1 = page_count
    return render(request, 'forum/page.html',{'page_1':page_1,'show_list':show_list,'page_count':page_count})

def page_before(request, page_1):
    print(page_1)
    page_1 -= 1
    a = Author.objects.all()
    page_count = a.count() / 2
    if page_1 == 0:
        page_1=1
    show_list = a[2 * (page_1 - 1): 2 * page_1]
    return render(request, 'forum/page.html',{'page_1':page_1,'show_list':show_list,'page_count':math.ceil(page_count)})

@require_http_methods(['POST'])
def page_dump(request, page_1):
    a = Author.objects.all()
    page_count = a.count()/2
    page_2 = request.POST['page']
    page_2 = int(page_2)
    if 0<page_2 <=page_count:
        show_list = a[2 * (page_2 - 1): 2 * page_2]
        return render(request, 'forum/page.html',{'page_1':page_2,'show_list':show_list,'page_count':math.ceil(page_count)})
    else:
        show_list = a[2 * (page_1 - 1): 2 * page_1]
        return render(request, 'forum/page.html',{'page_1':page_1,'show_list':show_list,'page_count':math.ceil(page_count)})
