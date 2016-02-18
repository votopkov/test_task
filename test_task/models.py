from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from autoslug.fields import AutoSlugField


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name',
                         editable=True,
                         unique=True
                         )
    description = models.TextField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('test_task:product_detail',
                       kwargs={'slug': self.slug})

    def product_like_count(self):
        return self.product_like.count()


class Likes(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product, related_name='product_like')


class Comment(models.Model):
    product = models.ForeignKey(Product)
    name = models.CharField(max_length=255)
    comment = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
