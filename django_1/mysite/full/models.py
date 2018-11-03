from django.db import models
from django.utils import timezone
class Foo(models.Model):
    pass

class Bar(models.Model):
    foo = models.OneToOneField(Foo, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)


    class Meta:
        default_related_name = 'bars'
        indexes = [
            models.Index(fields=['price', 'pub_date'],name='price_pub_date_idx')
        ]


class Blog(models.Model):
    name = models.CharField(max_length=50)
    tagline = models.TextField()

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=200)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return self.headline




