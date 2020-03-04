from django.db import models

# Create your models here.

class Article(models.Model):
    article_id=models.AutoField(primary_key=True)
    title=models.TextField()
    brief_content=models.TextField()
    content=models.TextField()
    publish_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class User(models.Model):
    openid=models.CharField(max_length=64,unique=True)
    nickname=models.CharField(max_length=64)
    focus_cities=models.TextField(default='[]')
    focus_constellations=models.TextField(default='[]')
    focus_stocks=models.TextField(default='[]')
