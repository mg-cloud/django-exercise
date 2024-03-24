from django.contrib import admin
from .models import Article, ArticleCategory, Sale

admin.site.register(ArticleCategory)
admin.site.register(Article)
admin.site.register(Sale)
