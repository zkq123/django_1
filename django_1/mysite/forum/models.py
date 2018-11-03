from django.db import models


from django.db import models
from django.utils import timezone

class BlogManage(models.Manager):

    def create_blog(self, name, tagline):
        blog = self.create(name=name, tagline=tagline)
        blog.tagline += 'add manager'
        blog.save()
        return blog


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()
    create_time = models.DateTimeField(default=timezone.now)
    objects = BlogManage()

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()
    test_datetime = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.headline

class Event(models.Model):
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
    )
    date = models.DateField()


