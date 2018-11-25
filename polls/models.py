import datetime
from django.db import models
from django.utils import timezone
from django_mysql.models import ListCharField
from django.core.validators import validate_comma_separated_integer_list
from users.models import CustomUser
from Django_hello import settings


class Question(models.Model):
    question_text = models.CharField(max_length=20)
    pub_date = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    question_sentence = models.TextField()
    question_picture = models.ImageField(upload_to='images/', null=True, blank=True)
    question_choices = ListCharField(base_field=models.CharField(max_length=100),
                                     size=5,
                                     max_length=(5 * 101))
    question_answers = models.CharField(validators=[validate_comma_separated_integer_list],
                                        max_length=question_choices.size + 1)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class SelectHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    select_date = models.DateTimeField()
    select_text = ListCharField(base_field=models.CharField(max_length=5),
                                size=5,
                                max_length=(5 * 6),)
    latest_solve_state = models.BooleanField(default=False)



"""class Choice(models.Model):


    def __str__(self):
        return self.choice_text

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default = 0)
"""
