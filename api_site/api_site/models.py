# This file contains classes that allow data to be transferred between the webpages
from django.db import models


class PassValAttr(models.Model):
    value = models.CharField(max_length=128)
    attribute = models.CharField(max_length=128)


class PassValAttrId(models.Model):
    ident = models.CharField(max_length=128)
    value = models.CharField(max_length=128)
    attribute = models.CharField(max_length=128)


class PassAll(models.Model):
    ident = models.CharField(max_length=128)
    book_url = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    ISBN = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    author_url = models.CharField(max_length=128)
    rating = models.CharField(max_length=128)
    rating_count = models.CharField(max_length=128)
    review_count = models.CharField(max_length=128)
    image_url = models.CharField(max_length=128)
    similar_books = models.CharField(max_length=128)
