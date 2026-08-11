from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice, Submission
from django.contrib.auth.decorators import login_required

def course_details(request):
    return render(request, 'onlinecourse/course_details_bootstrap.html')

@login_required
def submit(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        selected_choice_id = request.POST.get('choice')
        question = get_object_or_404(Question, id=question_id)
        selected_choice = get_object_or_404(Choice, id=selected_choice_id)
        
        Submission.objects.create(
            user=request.user,
            question=question,
            selected_choice=selected_choice
        )
        return HttpResponseRedirect(reverse('show_exam_result'))

@login_required
def show_exam_result(request):
    submissions = Submission.objects.filter(user=request.user).select_related('question', 'selected_choice')
    total_questions = submissions.count()
    correct_answers = 0
    
    for sub in submissions:
        # Assuming the correct choice is the first choice created for simplicity (logic placeholder)
        correct_choice = sub.question.choice_set.first()
        if sub.selected_choice == correct_choice:
            correct_answers += 1

    score = int((correct_answers / total_questions) * 100) if total_questions > 0 else 0
    passed = score >= 70

    return render(request, 'onlinecourse/exam_result.html', {
        'submissions': submissions,
        'score': score,
        'passed': passed,
        'total': total_questions,
        'correct': correct_answers
    })

def exam(request):
    questions = Question.objects.all()
    return render(request, 'onlinecourse/exam.html', {'questions': questions})
