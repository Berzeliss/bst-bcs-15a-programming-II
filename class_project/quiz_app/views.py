from django.shortcuts import render, get_object_or_404, redirect
from .models import *
import time
from django.contrib.auth.decorators import login_required
from .forms import QuizForm, QuestionFormSet


def index(request):
    return render(request, 'index.html')

def quiz_list(request, category):
    context = {'quizzes': Quiz.objects.filter(category=category)}
    return render(request, 'quiz_list.html', context)

def quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all().order_by("?")  # Randomize questions

    if request.method == 'POST':
        user_answers = request.POST  # Get user-submitted answers
        user_score = 0

        for question in questions:
            correct_answer = question.answers.filter(is_correct=True).first()
            user_answer = user_answers.get(f'question_{question.id}')
            
            if str(correct_answer.id) == user_answer:
                user_score += question.score

        result = Result.objects.create(
        user=request.user,
        quiz=quiz,
        score=user_score,
        attempted_at=time.time()
        )

        result_context = {'result':result}
        return render(request, 'result.html', result_context)
    
    elif request.method == 'GET':
        context = {'quiz': quiz, 'questions': questions}
        return render(request, 'quiz.html', context)

@login_required
def create_quiz(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST)
        if quiz_form.is_valid() and question_formset.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.created_by = request.user  # Set the creator
            quiz.save()
            questions = question_formset.save(commit=False)
            for question in questions:
                question.quiz = quiz  # Associate each question with the quiz
                question.save()
            return redirect('quiz_list', category=quiz.category)
    else:
        quiz_form = QuizForm()
        question_formset = QuestionFormSet()

    return render(request, 'create_quiz.html', {
        'quiz_form': quiz_form,
        'question_formset': question_formset,
    })
