from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, Question, Choice, Enrollment, Submission, Learner

def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})

def exam(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    questions = Question.objects.filter(lesson__course=course)
    return render(request, 'onlinecourse/exam.html', {'course': course, 'questions': questions})

@login_required
def submit(request, course_id):
    if request.method == 'POST':
        learner = Learner.objects.get(user=request.user)
        course = get_object_or_404(Course, pk=course_id)
        enrollment, created = Enrollment.objects.get_or_create(learner=learner, course=course)
        
        for key in request.POST:
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])
                chosen_choice_id = int(request.POST[key])
                question = get_object_or_404(Question, pk=question_id)
                chosen_choice = get_object_or_404(Choice, pk=chosen_choice_id)
                Submission.objects.create(
                    enrollment=enrollment,
                    question=question,
                    chosen_choice=chosen_choice
                )
        return HttpResponseRedirect(reverse('show_exam_result', args=(course_id,)))

@login_required
def show_exam_result(request, course_id):
    learner = Learner.objects.get(user=request.user)
    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(Enrollment, learner=learner, course=course)
    submissions = Submission.objects.filter(enrollment=enrollment)
    
    total_score = 0
    possible_score = 0
    
    for submission in submissions:
        total_score += submission.question.grade if submission.chosen_choice.is_correct else 0
        possible_score += submission.question.grade
    
    grade_percentage = (total_score / possible_score * 100) if possible_score > 0 else 0
    
    return render(request, 'onlinecourse/exam_result.html', {
        'course': course,
        'submissions': submissions,
        'grade_percentage': grade_percentage,
        'total_score': total_score,
        'possible_score': possible_score,
        'passed': grade_percentage >= 70
    })
