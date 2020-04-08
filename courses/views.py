from django.shortcuts import render,redirect
from django.db import transaction
from django.core.exceptions import PermissionDenied,SuspiciousOperation
from django.urls import reverse
from courses.models import Course,Section,Question,UserAnswer
from django.contrib.auth.models import User,auth

# Create your views here.
def home(request):
    return render(request,'home.html')

def do_section(request,section_id):
    section=Section.objects.get(id=section_id)
    return render(request,'course/do_section.html',{'section':section,})

def is_authenticated(request):
    if not request.user.is_authenticated:
        return False
    else:
        return True

def course_detail(request,course_id):
    course=Course.objects.get(id=course_id)
    section=course.section_set.all()
    return render(request,'courses/course_detail.html',{'section':section,})

def do_test(request, section_id):
    is_authenticated(request)
    section = Section.objects.get(id=section_id)
    if request.method == 'POST':
        data={}
        for key, value in request.POST.items():
            if key == 'csrfmiddlewaretoken':
                continue
            # {'question-1': '2'}
            question_id = key.split('-')[1]
            data[question_id] = value
        perform_test(request.user, data, section)
        return redirect(reverse('show_results', args=(section.id,)))
    return render(request, 'courses/do_test.html', {'section': section,})

def perform_test(user,data,section):
    with transaction.atomic():
        UserAnswer.objects.filter(user=user,question__section=section).delete()
        for question_id,answer_id in data.items():
            question=Question.objects.get(id=question_id)
            answer_id=int(answer_id)
            if answer_id not in question.answer_set.values_list('id',flat=True):
                raise SuspiciousOperation('Answer is not valid for this question')
            UserAnswer.objects.create(user=user,question=question,answer_id=answer_id,)

def course_list(request):
    if(is_authenticated(request)):
        courses=Course.objects.all()
        print(courses)
        return render(request,'courses/course_list.html',{'courses':courses,})
    else:
        return redirect('/')

def do_section(request,section_id):
    section=Section.objects.get(id=section_id)
    return render(request,'courses/do_section.html',{'section':section,})

def section_instructions(request,section_id):
    section=Section.objects.get(id=section_id)
    return render(request,'courses/section_instructions.html',{'section':section,})

def calculate_score(user,section):
    question=Question.objects.filter(section=section)
    correct_answer=UserAnswer.objects.filter(user=user,question__section=section,answer__correct=True)
    if(question.count()!=0):
        return (correct_answer.count()/question.count())*100
    else:
        return 0

def show_results(request,section_id):
    is_authenticated(request)
    section=Section.objects.get(id=section_id)
    return render(request,'courses/show_results.html',{'section':section,'score':calculate_score(request.user,section)})

def all_result(request,course_id):
    course=Course.objects.get(id=course_id)
    section=course.section_set.all()
    name=[]
    score=[]
    for n in section:
        name.append(n.title)
    for s in section:
        score.append(calculate_score(request.user,s))
    mylist=zip(name,score)
    return render(request,'courses/all_results.html',{'course':course,'mylist':mylist})
