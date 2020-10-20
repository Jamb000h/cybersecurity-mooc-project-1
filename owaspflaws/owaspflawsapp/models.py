from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    ingredients = models.TextField()
    directions = models.TextField()

    class Meta:
        db_table = "Recipe"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="comments")
    message = models.TextField()

    class Meta:
        db_table = "Comment"


class Log(models.Model):
    message = models.TextField()
    timestamp = models.TimeField(auto_now=True)

    class Meta:
        db_table = "Log"
