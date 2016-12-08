"""
UniversitiesApp Views

Created by Jacob Dunbar on 11/5/2016.
"""
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from . import models
from . import forms
from AuthenticationApp.models import MyUser, Student, Teacher


def getUniversities(request):
  if request.user.is_authenticated():
    universities_list = models.University.objects.all()
    context = {
      'universities': universities_list,
    }
    return render(request, 'universities.html', context)
  # render error page if user is not logged in
  return render(request, 'autherror.html')


def getUniversity(request):
  if request.user.is_authenticated():
    in_name = request.GET.get('name', 'None')
    in_university = models.University.objects.get(name__exact=in_name)
    is_member = in_university.members.filter(email__exact=request.user.email)
    is_studentorTeacher = False
    if request.user.is_student or request.user.is_professor:
      is_studentorTeacher = True
    context = {
      'university': in_university,
      'iseither':is_studentorTeacher,
      'userIsMember': is_member,
    }
    return render(request, 'university.html', context)
  # render error page if user is not logged in
  return render(request, 'autherror.html')


def getUniversityForm(request):
  # print("URL1:" + request.GET.get("redirect"))
  if request.user.is_authenticated():
    context = {"redirect" : str(request.GET.get("redirect"))}
    return render(request, 'universityform.html', context)
  # render error page if user is not logged in
  return render(request, 'autherror.html')


def getUniversityFormSuccess(request):
  # print("URL2 :" + request.GET.get("redirect"))
  if request.user.is_authenticated():
    if request.method == 'POST':
      form = forms.UniversityForm(request.POST, request.FILES)
      if form.is_valid():
        if models.University.objects.filter(name__exact=form.cleaned_data['name']).exists():
          return render(request, 'universityform.html', {'error': 'Error: That university name already exists!'})
        new_university = models.University(name=form.cleaned_data['name'],
                                           photo=request.FILES['photo'],
                                           description=form.cleaned_data['description'],
                                           website=form.cleaned_data['website'])
        new_university.save()
        context = {
          'name': form.cleaned_data['name'],
          'redirect': str(request.GET.get("redirect")),
        }
        return render(request, 'universityformsuccess.html', context)
      else:
        return render(request, 'universityform.html', {'error': 'Error: Photo upload failed!'})
    else:
      form = forms.UniversityForm()
    return render(request, 'universityform.html')
  # render error page if user is not logged in
  return render(request, 'autherror.html')


def joinUniversity(request):
  if request.user.is_authenticated():
    in_name = request.GET.get('name', 'None')
    in_university = models.University.objects.get(name__exact=in_name)
    in_university.members.add(request.user)
    in_university.save()
    curteach = Teacher.objects.get(teacher=request.user.id)
    prev_uni = curteach.university
    if prev_uni is not None:
      prev_uni.members.remove(request.user)
    curteach.university = in_university
    curteach.save()
    context = {
      'university': in_university,
      'userIsMember': True,
    }
    return render(request, 'university.html', context)
  return render(request, 'autherror.html')


def unjoinUniversity(request):
  if request.user.is_authenticated():
    in_name = request.GET.get('name', 'None')
    in_university = models.University.objects.get(name__exact=in_name)
    in_university.members.remove(request.user)
    in_university.save()
    curteach = Teacher.objects.get(teacher=request.user.id)
    prev_uni = curteach.university
    if prev_uni is not None:
      prev_uni.members.remove(request.user)
    curteach.university = None
    curteach.save()
    context = {
      'university': in_university,
      'userIsMember': False,
    }
    return render(request, 'university.html', context)
  return render(request, 'autherror.html')


def getCourse(request):
  if request.user.is_authenticated():
    course_id = request.GET.get('id')
    course = models.Course.objects.get(id=course_id)
    is_member = course.members.filter(email__exact=request.user.email)
    curid = Teacher()
    if request.user.is_professor == True:
      curid = Teacher.objects.get(teacher=request.user)
    else:
      curid = None
    context = {
      'course': course,
      'userInCourse': is_member,
      'user': request.user,
      'teacher': curid,
      'studentform': forms.AddStudentForm(),
    }
    return render(request, 'course.html', context)
  return render(request, 'autherror.html')


def courseForm(request):
  if request.user.is_authenticated():
    in_university_name = request.GET.get('name', 'None')
    if in_university_name == 'None':
      messages.warning(request, 'Please update your profile.')
      return HttpResponseRedirect('/home')
    else:
      in_university = models.University.objects.get(name__exact=in_university_name)
      context = {
        'university': in_university
      }
      return render(request, 'courseform.html', context)
      # render error page if user is not logged in
  return render(request, 'autherror.html')


def addCourse(request):
  if request.user.is_authenticated():
    if request.method == 'POST':
      form = forms.CourseForm(request.POST)
      if form.is_valid():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_teacher = models.Teacher.objects.get(teacher=request.user)
        if in_university.course_set.filter(tag__exact=form.cleaned_data['tag']).exists():
          return render(request, 'courseform.html',
                        {'error': 'Error: That course tag already exists at this university!'})
        new_course = models.Course(tag=form.cleaned_data['tag'],
                                   name=form.cleaned_data['name'],
                                   description=form.cleaned_data['description'],
                                   university=in_university,
                                   teacher=in_teacher
                                   )
        new_course.save()
        in_university.course_set.add(new_course)
        is_member = in_university.members.filter(email__exact=request.user.email)
        context = {
          'university': in_university,
          'userIsMember': is_member,
        }
        return render(request, 'university.html', context)
      else:
        return render(request, 'courseform.html', {'error': 'Undefined Error!'})
    else:
      form = forms.CourseForm()
      return render(request, 'courseform.html')
      # render error page if user is not logged in
  return render(request, 'autherror.html')


def removeCourse(request):
  if request.user.is_authenticated():
    in_university_name = request.GET.get('name', 'None')
    in_university = models.University.objects.get(name__exact=in_university_name)
    in_course_tag = request.GET.get('course', 'None')
    in_course = in_university.course_set.get(tag__exact=in_course_tag)
    in_course.delete()
    is_member = in_university.members.filter(email__exact=request.user.email)
    context = {
      'university': in_university,
      'userIsMember': is_member,
    }
    return render(request, 'university.html', context)
  # render error page if user is not logged in
  return render(request, 'autherror.html')


def joinCourse(request):
  if request.user.is_authenticated():
    in_university_name = request.GET.get('name', 'None')
    in_university = models.University.objects.get(name__exact=in_university_name)
    in_course_tag = request.GET.get('course', 'None')
    in_course = in_university.course_set.get(tag__exact=in_course_tag)
    in_course.members.add(request.user)
    in_course.save();
    request.user.course_set.add(in_course)
    request.user.save()
    context = {
      'university': in_university,
      'course': in_course,
      'userInCourse': True,
    }
    return render(request, 'course.html', context)
  return render(request, 'autherror.html')


def unjoinCourse(request):
  curid = request.GET.get('id','None')
  curmyuser = MyUser.objects.get(id=curid)
  # if request.user.is_authenticated():
  in_university_name = request.GET.get('name', 'None')
  in_university = models.University.objects.get(name__exact=in_university_name)
  in_course_tag = request.GET.get('course', 'None')
  in_course = in_university.course_set.get(tag__exact=in_course_tag)
  in_course.members.remove(curmyuser)
  in_course.save()
  curmyuser.course_set.remove(in_course)
  curmyuser.save()
  context = {
    'university': in_university,
    'course': in_course,
    'userInCourse': False,
  }
  return render(request, 'course.html', context)
  # return render(request, 'autherror.html')

def getTeachersCourses(request):
  if request.user.is_authenticated():
    in_teacher = models.Teacher.objects.get(teacher=request.user)
    courses = models.Course.objects.filter(teacher=in_teacher)

    context = {
      'courses': courses,
      'teacher': request.user,
    }
    return render(request, 'course_list.html' , context)
  return render(request, 'autherror.html')