from django.db import models
from django.utils import timezone
import datetime
# Create your models here.
class Question(models.Model):
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    def __str__(self):
        return  self.question_text
    question_text = models.CharField(max_length=100)
    pub_date = models.DateTimeField('datepublished')

class Choice(models.Model):
    def __str__(self):
        return "下联：%s, 投票：%s, 问题ID：%s" % (self.choice_text, self.votes, self.question_id)
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text =models.CharField(max_length = 200)
    votes = models.IntegerField(default=0)
