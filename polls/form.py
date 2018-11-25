from .models import Question
from django import forms


class MyForm(forms.ModelForm):
    class Meta:
        model = Question
        fields =["question_sentence", "question_picture", "question_choices", "question_answers"]
        widgets = {"question_picture": forms.FileInput(attrs={'multiple': True}),
                   "question_choices":forms.Textarea}
