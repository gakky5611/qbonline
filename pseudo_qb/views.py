from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic.edit import CreateView
from django.utils import timezone
from django.urls import reverse_lazy
# Create your views here.
from polls.models import Question
from polls.form import MyForm


@login_required
def PracticeView(request):
    return render(request, 'pseudo_qb/practice.html',)


class RegisterView(LoginRequiredMixin, CreateView):
    login_url = "login"
    model = Question
    form_class = MyForm
    template_name = 'pseudo_qb/register.html'
    success_url = reverse_lazy("pseudo_qb:register")



