from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):

    def show_solved_question_id(self):
        for sel in self.selecthistory_set.all():
            print(sel.question_id)
