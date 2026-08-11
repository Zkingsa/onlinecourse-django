from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Enrollment, Submission

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'description')

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('title', 'course')

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'lesson', 'grade')

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('learner', 'course', 'date_enrolled')

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Submission)
