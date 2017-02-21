from django.contrib import admin
from .models import *

admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(Relation)
admin.site.register(Users)
admin.site.register(Comments)
admin.site.register(CommentsToArticles)
