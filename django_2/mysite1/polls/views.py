from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from . models import Question, Choice
from django.urls import reverse
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:10]
    context = {
        "latest_question_list":latest_question_list
    }
    return render(request, "polls1/index.html", context)
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('没有你所选的问题')
    return render(request, 'polls1/detail.html', {'question':question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls1/detail.html', {
            'question':question,
            'error_message':"请选择正确选项"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls1:results', args=(question.id,)))
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls1/results.html', {'question':question})