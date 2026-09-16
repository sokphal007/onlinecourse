from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Course, Lesson, Question, Choice, Submission

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    # ទទួលយក ID នៃ Choice ដែលបានជ្រើសរើសពីសំណុំបែបបទ (Form)
    choice_ids = request.POST.getlist('choice_ids')
    
    # បង្កើត Submission object ថ្មីសម្រាប់ผู้เรียน
    submission = Submission.objects.create(enrollment=None) # ឬផ្អែកតាមការកំណត់គម្រោងរបស់អ្នក
    
    # ពិនិត្យ និងរក្សាទុកជម្រើសដែលបានជ្រើសរើស
    for choice_id in choice_ids:
        choice = Choice.objects.get(pk=choice_id)
        submission.choices.add(choice)
        
    return HttpResponseRedirect(reverse('onlinecourse:show_exam_result', args=([course.id, submission.id])))

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    context = {
        'course': course,
        'submission': submission,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
