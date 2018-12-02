from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, FormView
from django.utils import timezone
from django.http import HttpResponseRedirect
from .models import Question, SelectHistory
from users.models import CustomUser
from .form import FinalForm,MyPicForm,MyForm
import re


class NullListException(Exception):
    pass


def check_model_list(model_list):
    if not model_list:
        raise NullListException


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = 'login'
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        self.request.session["active_index"] = 0
        if "num_index" in self.request.session:
            num_index = int(self.request.session["num_index"])
        else:
            num_index = 10
            self.request.session["num_index"] = num_index
        if "order_state" in self.request.session:
            order_state = self.request.session["order_state"]
        else:
            order_state = "new"
            self.request.session["order_state"] = order_state

        if order_state == "new":
            q_list = Question.objects.filter(question_sub=0).order_by('-pub_date')[:num_index]
        else:
            q_list = Question.objects.filter(question_sub=0).order_by('pub_date')[:num_index]

        for q in q_list:
            states = q.selecthistory_set.all().filter(user_id=self.request.user.id)

            try:
                sel = states.order_by('-select_date')[0]
                solved_state = True
                if sel.select_text == q.question_answers:
                    q.solver = True
                else:
                    q.solver = False
            except IndexError:
                solved_state = False
            q.latest_solve_state = solved_state

        return q_list

    def user_score_registrations(self):

        final_data = {}
        for u in CustomUser.objects.all():
            score = 0
            for q in Question.objects.all():
                if q.question_answers.split(',') \
                        == q.selecthistory_set.all().order_by('-select_date')[0].select_text:
                    score += 1
            final_data[u.username] = score

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "user_score_registrations": self.user_score_registrations
        })
        return context

    def post(self, request):
        request.session["active_index"] = 0
        request.session["num_index"] = self.request.POST["num_index"]
        request.session["order_state"] = self.request.POST["order_state"]
        q_list = self.get_queryset()
        context = {'latest_question_list': q_list}
        self.object_list = q_list
        return self.render_to_response(context)


class DetailView(LoginRequiredMixin, generic.DetailView):
    login_url = 'login'
    model = Question
    template_name = 'polls/detail.html'


class DetailListView(LoginRequiredMixin, generic.ListView):
    login_url = 'login'
    context_object_name = "question_list"
    template_name = 'polls/detail_list.html'
    q_list = []
    active_index = 0

    def get_queryset(self):
        if "num_index" in self.request.session:
            num_index = int(self.request.session["num_index"])
        else:
            num_index = 5
        if "order_state" in self.request.session:
            order_state = self.request.session["order_state"]
        else:
            order_state = "new"

        if order_state == "new":
            self.q_list = Question.objects.filter(question_sub=0).order_by('-pub_date')[:num_index]
        else:
            self.q_list = Question.objects.filter(question_sub=0).order_by('pub_date')[:num_index]
        print(self.q_list)
        return self.q_list

    def get_context_data(self, **kwargs):
        if "active_index" in self.request.session:
            self.active_index = self.request.session["active_index"]
        self.active_index = kwargs["question_id"]

        self.request.session["active_index"] = self.active_index
        context = super().get_context_data(**kwargs)
        questions = Question.objects.filter(question_series=self.q_list[self.active_index].question_text)
        if len(questions) > 1:
            match = re.findall(r'[0-9]+', questions.reverse().first().question_text)

            title = questions[0].question_text + "-" + match[-1]
        else:
            title = questions[0].question_text
        context.update({"questions": questions,
                        "active_index": self.active_index,
                        "title_text": title})
        return context

    def post(self, request, **kwargs):
        if request.POST.getlist('checks'):
            selected_qid = request.POST.getlist('checks')
        else:
            if self.request.session["selected_id"]:
                selected_qid = self.request.session["selected_id"]
            else:
                return redirect("polls:index")
        self.request.session["selected_id"] = selected_qid
        qids = [int(s) for s in selected_qid]
        self.q_list = Question.objects.filter(pk__in=qids)

        if "order_state" in self.request.session:
            order_state = self.request.session["order_state"]
        else:
            order_state = "new"

        if order_state == "new":
            self.q_list = self.q_list.order_by('-pub_date')
        else:
            self.q_list = self.q_list.order_by('pub_date')
        if kwargs['question_id'] == 0:
            pass
        else:
            self.active_index = kwargs['question_id']
        questions = Question.objects.filter(question_series=self.q_list[self.active_index].question_text)
        if len(questions) > 1:
            match = re.findall(r'[0-9]+', questions.reverse().first().question_text)

            title = questions[0].question_text + "-" + match[-1]
        else:
            title = questions[0].question_text
        self.object_list = self.q_list
        context = {"questions": questions,
                   "question_list": self.q_list,
                   "active_index": self.active_index,
                   "title_text": title}

        id_list = []
        for obj in self.object_list:
            id_list.append(obj.id)
        self.request.session["id_list"] = id_list
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        if kwargs["active_id"] != 0:
            q = Question.objects.get(pk=kwargs["active_id"])
            questions = Question.objects.filter(question_series=q.question_text)
            if len(questions) > 1:
                match = re.findall(r'[0-9]+', questions.reverse().first().question_text)
                title = questions[0].question_text + "-" + match[-1]
            else:
                title = questions[0].question_text
            context = {"questions": questions,
                       "question_list": q,
                       "active_index": 0,
                       "title_text": title}
            return self.render_to_response(context)

        self.object_list = self.get_queryset()
        id_list = []
        for obj in self.object_list:
            id_list.append(obj.id)
        self.request.session["id_list"] = id_list

        allow_empty = self.get_allow_empty()

        if not allow_empty:
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data(**kwargs)
        return self.render_to_resopnse(context)



class RegisterView(LoginRequiredMixin, FormView):
    login_url = "login"
    form_class = FinalForm
    template_name = 'polls/register.html'
    success_url = reverse_lazy("polls:register")

    def form_valid(self, form):

        f = MyForm(self.request.POST)
        k = MyPicForm(self.request.POST,self.request.FILES)
        f.save()
        k.save()
        return super().form_valid(form)


@login_required
def scoreview(request):
    context = {"users": CustomUser.objects.all()}
    return render(request, 'polls/listing.html', context)


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


@login_required
def aggregate(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    user = request.user
    questions = Question.objects.filter(question_series=q.question_text)
    active_index = 0
    selected_list = []
    q_list = []
    if "active_index" in request.session:
        active_index = request.session["active_index"]

    for x in request.session["id_list"]:
        q_list.append(Question.objects.get(pk=x))
    if len(questions) > 1:
        match = re.findall(r'[0-9]+', questions.reverse().first().question_text)

        title = questions[0].question_text + "-" + match[-1]
    else:
        title = questions[0].question_text

    for question in questions:
        try:
            selected_choice = request.POST.getlist('choices'+str(question.id))
            selected_list.append(selected_choice)
            check_model_list(selected_choice)
            print(request.POST)
            selecthistory = SelectHistory(question_id=question_id,
                                          select_date=timezone.now(),
                                          select_text=selected_choice,
                                          user_id=user.id,
                                          select_status=0)
        except NullListException:

            return render(request, 'polls/detail_list.html', {
                'questions': questions,
                'question_list': q_list,
                'error_message': "You didn't select a choice",
                'title': title,
                'active_index' : active_index
            })
        else:
            if question.question_answers == selected_choice:
                selecthistory.select_status = 1
            user.save()
            selecthistory.save()
            user.selecthistory_set.add(selecthistory)
            question.selecthistory_set.add(selecthistory)

    return render(request, "polls/detail_list.html", {
        'questions': questions,
        'question_list': q_list,
        'selected_answer': selected_list,
        "active_index": active_index,
        "title_text": title,
        "applicationisValid": 1})
