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

QuestionFormSet = inlineformset_factory(Quiz, Question, fields=('text', 'score'), extra=3)
AnswerFormSet = inlineformset_factory(Question, Answer, fields=('text', 'is_correct'), extra=3)
