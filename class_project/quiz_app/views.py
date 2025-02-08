from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.utils import timezone 
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def index(request):
    return render(request, 'index.html')

def quiz_list(request, category):
    context = {'quizzes': Quiz.objects.filter(category=category)}
    return render(request, 'quiz_list.html', context)

def quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all().order_by("?")  # Randomize questions

    if request.method == 'POST':

        result = Result.objects.create(
            user=request.user, quiz=quiz, attempted_at=timezone.now()
            )
        
        user_score = 0
        for question in questions:
            correct_answer = question.answers.filter(is_correct=True).first()
            user_answer_id = request.POST.get(f'question_{question.id}')
            answer = question.answers.filter(id=user_answer_id).first()

            if answer:
                UserAnswer.objects.create(
                    result=result, question=question, answer=answer
                    )

            
            if str(correct_answer.id) == user_answer_id:
                user_score += question.score

        result.score=user_score
        result.save()

        # Redirect to the result page after submission
        return redirect('result', result_id=result.id)
    
    elif request.method == 'GET':
        context = {'quiz': quiz, 'questions': questions}
        return render(request, 'quiz.html', context)

def result(request, result_id):
    result = get_object_or_404(Result, id=result_id, user=request.user)
    questions = result.quiz.questions.all()
    total_score = sum(question.score for question in questions)

    question_answers = []
    for question in questions:
        correct_answer = question.answers.filter(is_correct=True).first()
        user_answer = result.user_answers.filter(question=question).first()

        question_answers.append({
            'question': question.text,
            'user_answer': user_answer.answer.text if user_answer else "No answer",
            'correct_answer': correct_answer.text if correct_answer else "No correct answer",
        })

    percentage_score = (result.score / total_score) * 100 if total_score > 0 else 0

    context = {
        'result': result,
        'question_answers': question_answers,
        'total_score': total_score,
        'percentage_score': round(percentage_score, 2)
    }
    return render(request, 'result.html', context)


@login_required
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    results = Result.objects.filter(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
        context = {
            'profile': profile,
            'form': form,
            'results': results
        }
        return render(request, 'profile.html', context)

@login_required
def create_quiz(request):
    if request.method == "POST":
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST, prefix='questions')

        if quiz_form.is_valid() and question_formset.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            question_formset.instance = quiz

            for question_form in question_formset:
                question = question_form.save(commit=False)
                question.quiz = quiz
                question.save()

                # handle the answers
                if question_form.nested.is_valid():
                    question_form.nested.instance = question
                    question_form.nested.save()

            return redirect('quiz_list', category=quiz.category)
        else:
            print("Quiz form errors:", quiz_form.errors)
            print("Question formset errors:", question_formset.errors)
            for question_form in question_formset:
                print("Answer formset errors:", question_form.nested.errors)

    else:
        quiz_form = QuizForm()
        question_formset = QuestionFormSet(prefix='questions')

    return render(request, 'create_quiz.html', {
        'quiz_form': quiz_form,
        'question_formset': question_formset
    })


"""Authentication"""
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Account created for {user.username}. Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
