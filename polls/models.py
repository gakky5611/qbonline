import datetime
from django.db import models
from django.utils import timezone
from django_mysql.models import ListCharField
from users.models import CustomUser
from Django_hello import settings


class Question(models.Model):
    question_text = models.CharField(blank=False, max_length=20)
    pub_date = models.DateTimeField(null=True, auto_now_add=True)
    question_sentence = models.TextField()
    question_choices = ListCharField(base_field=models.CharField(max_length=100),
                                     size=5,
                                     max_length=(5 * 101))
    question_answers = ListCharField(base_field=models.CharField(max_length=10),
                                     size=5,
                                     max_length=(5 * 11))
    question_commentary = models.TextField()
    question_series = models.CharField(blank=True, max_length=20)
    question_sub = models.IntegerField(default=0)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class SelectHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    select_date = models.DateTimeField()
    select_text = ListCharField(base_field=models.CharField(max_length=10),
                                size=5,
                                max_length=(5 * 11),)
    select_status = models.IntegerField()


class Picture(models.Model):
    picture = models.ImageField(upload_to='images/', null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

"""class Choice(models.Model):


    def __str__(self):
        return self.choice_text

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default = 0)
"""
