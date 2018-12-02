from .models import Question, Picture
from django import forms


class MyForm(forms.ModelForm):
    class Meta:
        model = Question
        fields =["question_text", "question_sentence", "question_choices", "question_answers","question_commentary",
                 "question_series"]
        widgets = {"question_choices":forms.Textarea}

    def save(self, commit=True):
        super().save()
        print(self.data)
        print(self.fields["question_text"])
        qs = self.data["question_series"]
        if not qs:
            self.instance.question_series = self.data["question_text"]
            print(self.instance.question_series)
        else:
            if self.data["question_series"] != self.data["question_text"]:
                self.isntance.question_sub = 1
        self.instance.save()



class MyPicForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ["picture"]
        widgets = {"picture": forms.ClearableFileInput(attrs={'multiple': True})}

    def save(self, commit=True):
        try:
            pictures = self.files.pop("picture")
            self.instance.question_id = Question.objects.all().reverse().first().id
            for p in pictures:
                obj = Picture(question_id=self.instance.question_id)
                obj.picture = p
                print(obj.picture)
                obj.save()
        except KeyError:
            pass

class MyMixedForm(forms.Form):
    form_classes =[]

    def __init__(self, *args, **kwargs):
        super(MyMixedForm, self).__init__(*args, **kwargs)

        for f in self.form_classes:
            name = f.__name__.lower()
            setattr(self, name, f(*args, **kwargs))
            form = getattr(self, name)
            self.fields.update(form.fields)
            self.initial.update(form.initial)

    def is_valid(self):
        isValid = True
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            if not form.is_valid():
                isValid = False

        if not super(MyMixedForm, self).is_valid():
            isValid = False
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            self.errors.update(form.errors)
        return isValid

    def clean(self):
        cleaned_data = super(MyMixedForm, self).clean()
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self,name)
            cleaned_data.update(form.cleaned_data)
            return cleaned_data


class FinalForm(MyMixedForm):
    form_classes = [MyForm, MyPicForm]