"""CSCapstone Views

Created by Harris Christiansen on 9/18/16.
"""
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from UniversitiesApp import models
from CompaniesApp.models import Company

from .forms import TeacherForm, StudentForm, EngineerForm

from AuthenticationApp.models import Teacher, Student, Engineer

def getIndex(request):
  if request.user.is_authenticated:
    return HttpResponseRedirect("/home")
  return render(request, 'index.html', {
        'foo': 'bar',
    })

def getTable(request):
  return render(request, 'table.html')

def getForm(request):
  return render(request, 'form.html')

def getHome(request):
    a = None
    type = None
    profiler_id = request.GET.get('id', 'None')
    if profiler_id == 'None':
      if request.user.is_professor == True:
          type = "Teacher"
          a = Teacher.objects.filter(teacher=request.user)[0]
      elif request.user.is_student == True:
          type = "Student"
          a = Student.objects.get(user_id=request.user)
      elif request.user.is_engineer == True:
        type = "Engineer"
        a = Engineer.objects.get(engID=request.user)

      return render(request, 'home.html',{
          'profile': a,
          'user': request.user,
          'type': type,
          'request_user': None,
      })
    else:
      myuser = models.MyUser.objects.get(id=profiler_id)
      if request.user.is_professor == True:
        type = "Teacher"
        a = Teacher.objects.filter(teacher=myuser)[0]
      elif request.user.is_student == True:
        type = "Student"
        a = Student.objects.get(user_id=request.user)
      elif request.user.is_engineer == True:
        type = "Engineer"
        a = Engineer.objects.get(engID=request.user)

      return render(request, 'home.html', {
        'profile': a,
        'user': myuser,
        'type': type,
        'request_user': request.user,
      })

def profile_edit(request):
    current_user = request.user
    form = None

    if current_user.is_professor:
        form = TeacherForm(request.POST or None)
        print("The form is valid:  " + str(form.is_valid()))
        if form.is_valid():
          print(form.cleaned_data['university'])
          university_id = form.cleaned_data['university']
          university = models.University.objects.get(id=university_id)
          department = form.cleaned_data['department']
          contact = form.cleaned_data['contact']
          almamater = form.cleaned_data['almamater']
          # pic = request.FILES['photo']

          t = Teacher.objects.get(teacher=request.user)
          t.university = university
          t.department = department
          t.contact = contact
          # t.pic = pic
          t.almamater = almamater
          t.save()
          messages.success(request, 'Success, your profile was saved!')

          return render(request, 'home.html', {
            'profile': t,
            'user': request.user,
            'type': 'Teacher',
          })
    elif current_user.is_student:
        form = StudentForm(request.POST or None)
        if form.is_valid():
          university_id = form.data['university']
          university = models.University.objects.get(id=university_id)
          major = form.cleaned_data['major']
          skills = form.cleaned_data['skills']
          resume = form.data['resume']
          experience = form.cleaned_data['experience']
          year = form.cleaned_data['year']
          # pic = request.FILES['photo']
          s = Student.objects.get(user=request.user)
          s.major = major
          s.skills = skills
          s.resume = resume
          # s.pic = pic
          s.experience = experience
          s.university = university
          s.year = year
          s.save()

          messages.success(request, 'Success, your profile was saved!')
          return render(request, 'home.html', {
            'profile': s,
            'user': request.user,
            'type': 'Student',
          })
    elif current_user.is_engineer:
        form = EngineerForm(request.POST or None)
        if form.is_valid():
          resume = form.cleaned_data['resume']
          experience = form.cleaned_data['experience']
          company = Company.objects.get(id=form.cleaned_data['company'])
          photo = form.cleaned_data['photo']
          contact = form.cleaned_data['contact']
          almamater = form.cleaned_data['almamater']
          bio = form.cleaned_data['bio']
          e = Engineer.objects.get(engID=request.user)
          e.company = company
          e.resume = resume
          e.experience = experience
          e.photo = photo
          e.contact = contact
          e.bio = bio
          e.almamater = almamater
          e.save()

          messages.success(request, 'Success, your profile was saved!')
          return render(request, 'home.html', {
            'profile': e,
            'user': request.user,
            'type': 'Engineer',
          })
    context = {
        "form": form,
        "page_name": "Update Your Profile Info",
        "button_value": "Update",
        "links": ["Home"],
        "user": current_user,
    }
    return render(request, 'update.html', context)