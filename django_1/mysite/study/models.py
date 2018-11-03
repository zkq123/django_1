from django.db import models
from django.utils import timezone

class LoginUser(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)

class LoginUserDetail(models.Model):
    age = models.IntegerField(default=0)
    birthday = models.DateField(default=timezone.now)
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    login_user = models.OneToOneField(LoginUser, on_delete=models.CASCADE)

class Author(models.Model):
    real_name = models.CharField(max_length=50)

class Book(models.Model):
    author = models.ManyToManyField(Author)
    book_name = models.CharField(max_length=50, default='')

class Foo(models.Model):
    pass

class Bar(models.Model):
    foo = models.ManyToManyField(Foo)

    class Meta:
        default_related_name = 'bars'

class Water(models.Model):
    clean = models.CharField(max_length=50)

class Fish(models.Model):
    water = models.ForeignKey(Water, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'bars'



