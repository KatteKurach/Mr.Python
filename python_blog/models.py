from __future__ import unicode_literals

from django.db import models

class Article(models.Model):
    header = models.CharField(max_length = 200)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add = True, blank = True)

class Tag(models.Model):
    value = models.CharField(max_length = 200)

class Relation(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE,)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE,)

class Users(models.Model):
    username = models.CharField(max_length = 200)
    email = models.EmailField()
    password = models.CharField(max_length = 100)

class Comments(models.Model):
    username = models.ForeignKey('Users', on_delete=models.CASCADE,)
    value = models.TextField()

class CommentsToArticles(models.Model):
    arcticle = models.ForeignKey('Article', on_delete=models.CASCADE,)
    comment = models.ForeignKey('Comments', on_delete=models.CASCADE,)

class Likes(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE,)
    user = models.ForeignKey('Users', on_delete=models.CASCADE,)
