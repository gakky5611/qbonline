from django.contrib import admin

# Register your models here.
from .models import Question, SelectHistory, Picture

admin.site.register(Question)
admin.site.register(SelectHistory)
admin.site.register(Picture)