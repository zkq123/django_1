from django.db import models
from django.utils import timezone
import datetime
# Create your models here.a

class Question(models.Model):
    # def is_new(self):
    #     return self.pub_date>= timezone.now() + datetime.timedelta(hours= -1)
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    def __str__(self):
        return  self.question_text
    question_text = models.CharField(max_length=100)
    pub_date = models.DateTimeField('datepublished')
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    def __str__(self):
        return "选项：%s, 投票：%s, 问题ID：%s" % (self.choice_text, self.votes, self.question_id)
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text =models.CharField(max_length = 200)
    votes = models.IntegerField(default=0)

