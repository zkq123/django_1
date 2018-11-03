from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.db.models import F
from django.views.decorators.http import require_http_methods

# Create your views here.
def index(request):
    lastest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "lastest_question_list": lastest_question_list
    }
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    if request.user.is_anonymous:
        print("我没登陆啊啊啊啊啊")
    else:
        print("很好，很强大，你已登录")

    # 判断用户是否登录。true 则为登录
    if request.user.is_authenticated:
        print(request.user)
    else:
        print("我还没登录啊啊啊啊啊啊啊啊啊啊啊啊啊啊")
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("没有你所选的问题")
    return render(request, 'polls/detail.html', {'question':question})

    # return HttpResponse("Detail is running %s" % question_id)
@require_http_methods(["GET", "POST"])
#  会报错因为发送的为post请求，在这里只接受get请求。
def vote(request, question_id):
    print(request.POST['area'])
    print('====================================')
    print(request.COOKIES)
    print(request.COOKIES.get('sessionid'))
    request.session['loginuser'] = 'zkq'
    if request.session.get('loginuser'):
        print('username=',request.session.get('loginuser'))
    else:
        print('未登录')
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question':question,
            'error_message':"请选择正确选项"
        })
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    # return HttpResponse("Vote is running %s" % question_id)

def results(request, question_id):
    print(request.COOKIES)
    print(request.COOKIES.get('sessionid'))
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})





