from django import forms
from .models import *
from django.forms import inlineformset_factory

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

QuestionInlineFormSet = inlineformset_factory(Quiz, Question, form=QuestionForm, extra=1, can_delete=True)
AnswerInlineFormSet = inlineformset_factory(Question, Answer, form=AnswerForm, extra=4, can_delete=True)
