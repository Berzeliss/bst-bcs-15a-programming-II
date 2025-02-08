from django import forms
from .models import *
from django.forms import inlineformset_factory, BaseInlineFormSet

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'category']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'score']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']


# handle nested inlines
AnswerFormSet = inlineformset_factory(Question, Answer, form=AnswerForm, extra=1)

class BaseQuestionFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.nested = AnswerFormSet(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix=f'answers-{form.prefix}-{AnswerFormSet.get_default_prefix()}'
        )

QuestionFormSet = inlineformset_factory(Quiz, Question, form=QuestionForm, formset=BaseQuestionFormSet, extra=1)
