from django.db import models
from django.utils import timezone
import datetime


class Question(models.Model):
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    question_text = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default=0)

class Person(models.Model):
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large')
    )
    second_name = models.IntegerField(blank=True, default=0)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, default='')
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES, default='')

class Musician(models.Model):
    one_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=50)
    two_name = models.CharField(max_length=50)

class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()

    class Meta:
        ordering = ['-id']

class Alum(models.Model):
    age = models.IntegerField()
    name = models.CharField(max_length=3, null=False)

class Human(models.Model):
    name = models.CharField(max_length=50)

class Man(Human):
    height = models.IntegerField(default=0)

class Women(Human):
    weight = models.IntegerField(default=0)

class Article(models.Model):
    article_id = models.AutoField(primary_key=True)


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)

class  BookReview(Book, Article):
    page_count = models.IntegerField(default=0)

class BookA(models.Model):
    page_count = models.IntegerField()

class BookB(BookA):
    page_size = models.IntegerField()

class BookC(BookB):
    book_name = models.CharField(max_length=50)










