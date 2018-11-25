from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, SelectHistory
from users.models import CustomUser

class NullListException(Exception):
    pass


def check_list(list):
    if not list:
        raise NullListException


class IndexView(LoginRequiredMixin,generic.ListView):
    login_url = 'login'
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    correct_num = 0
    total_num = 0
    index_num = 10

    def get_queryset(self):
        q_list = Question.objects.order_by('-pub_date')[:self.index_num]
        self.request.session["index_num"] = len(q_list)
        for q in q_list:
            states = q.selecthistory_set.all().filter(user_id=self.request.user.id)

            try:
                sel = states.order_by('-select_date')[0]
                self.total_num += 1
                solved_state = sel.latest_solve_state
                answer = q.question_answers.split(',')

                if sel.select_text == answer:
                    q.solver = True
                    self.correct_num += 1
                else:
                    q.solver = False
            except IndexError:
                solved_state = False
            q.latest_solve_state = solved_state

        return q_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"total_num": self.total_num,
                        "correct_num": self.correct_num,
                        "index_num": self.index_num
                        })
        return context


class DetailView(LoginRequiredMixin, generic.DetailView):
    login_url = 'login'
    model = Question
    template_name = 'polls/detail.html'

    def get_context_data(self, **kwargs):
        index_num = self.request.session["index_num"]
        dummy_text = index_num *'*'
        context = super().get_context_data(**kwargs)
        context.update({"q_num": self.request.session["index_num"],
                        "dummy_text": dummy_text})
        return context

@login_required
def scoreview(request):
    context ={"users" : CustomUser.objects.all()}
    return render(request,'polls/listing.html',context)

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@login_required
def aggregate(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = request.user

    try:
        selected_choice = request.POST.getlist('choices')
        check_list(selected_choice)
        selecthistory = SelectHistory(question_id =question_id,
                                      select_date=timezone.now(),
                                      select_text=selected_choice,
                                      user_id=user.id)

    except NullListException:
        return render(request, 'polls/detail.html', {
                      'question': question,
                      'error_message': "You didn't select a choice"
        })
    else:
        selecthistory.latest_solve_state = True
        selecthistory.save()
        user.selecthistory_set.add(selecthistory)
        question.selecthistory_set.add(selecthistory)

        print(selected_choice)
        next_id = question.id + 1
        print(next_id)
        return HttpResponseRedirect(reverse('polls:detail', args=(next_id,)))
