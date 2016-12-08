"""CSCapstone Views

Created by Harris Christiansen on 9/18/16.
"""
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from UniversitiesApp.models import Course, University
from CompaniesApp.models import Company
from AuthenticationApp.models import MyUser
from GroupsApp.models import Group
from ProjectsApp.models import Project


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
      class_list = []
      course_list = []
      project_list = []
      groups_list = []
      if request.user.is_professor == True:
        type = "Teacher"
        a = Teacher.objects.filter(teacher=request.user)[0]
        class_list = list(Course.objects.filter(teacher=a))
      elif request.user.is_student == True:
        type = "Student"
        a = Student.objects.get(user_id=request.user)
        for course in Course.objects.all():
          if request.user in course.members.all():
            course_list.append(course)
        for group in Group.objects.all():
          if request.user in group.members.all():
            groups_list.append(group)
      elif request.user.is_engineer == True:
        type = "Engineer"
        a = Engineer.objects.get(engID=request.user)

        for project in Project.objects.all():
          if a.id == project.engID.id:
            project_list.append(project)

      return render(request, 'home.html',{
          'profile': a,
          'user': request.user,
          'type': type,
          'request_user': None,
          'classes': class_list,
          'courses': course_list,
          'projects': project_list,
          'groups': groups_list,
      })
    else:
      class_list = []
      course_list = []
      project_list = []
      groups_list = []

      myuser = MyUser.objects.get(id=profiler_id)
      if request.user.is_professor == True:
        type = "Teacher"
        a = Teacher.objects.filter(teacher=myuser)[0]
        class_list = list(Course.objects.filter(teacher=a))
      elif request.user.is_student == True:
        type = "Student"
        a = Student.objects.get(user_id=myuser)
        for course in Course.objects.all():
          if request.user in course.members.all():
            course_list.append(course)
        for group in Group.objects.all():
          if request.user in group.members.all():
            groups_list.append(group)
      elif request.user.is_engineer == True:
        type = "Engineer"
        a = Engineer.objects.get(engID=myuser)
        for project in Project.objects.all():
          if request.user.id == project.engID:
            project_list.append(project)

      return render(request, 'home.html', {
        'profile': a,
        'user': myuser,
        'type': type,
        'request_user': request.user,
        'classes': class_list,
        'courses': course_list,
        'projects': project_list,
        'groups': groups_list,
      })

def profile_edit(request):
    current_user = request.user
    form = None

    if current_user.is_professor:
        if request.method == 'POST':
          form = TeacherForm(request.POST, request.FILES)
          if form.is_valid():
            print(form.cleaned_data['university'])
            # print(form)
            university_id = form.cleaned_data['university']
            university = University.objects.get(id=university_id)
            department = form.cleaned_data['department']
            contact = form.cleaned_data['contact']
            almamater = form.cleaned_data['almamater']


            pic = request.FILES['photo']
            t = Teacher.objects.get(teacher=request.user)
            if t.university is not None:
                prev_uni = t.university
                prev_uni.members.remove(current_user)
            university.members.add(current_user)
            t.university = university
            t.department = department
            t.contact = contact
            t.pic = pic
            t.almamater = almamater
            t.save()
            messages.success(request, 'Success, your profile was saved!')
            return render(request, 'home.html', {
              'profile': t,
              'user': request.user,
              'type': 'Teacher',
            })
        context = {
          "form": TeacherForm(),
          "page_name": "Update Your Profile Info",
          "button_value": "Update",
          "links": ["Home"],
          "user": current_user,
        }
        return render(request, 'update.html', context)
    elif current_user.is_student:
      if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
          university_id = form.data['university']
          university = University.objects.get(id=university_id)
          major = form.cleaned_data['major']
          skills = form.cleaned_data['skills']
          resume = form.data['resume']
          experience = form.cleaned_data['experience']
          year = form.cleaned_data['year']
          pic = request.FILES['photo']
          s = Student.objects.get(user=request.user)
          if s.university is not None:
              prev_uni = s.university
              prev_uni.members.remove(current_user)
          university.members.add(current_user)
          s.major = major
          s.skills = skills
          s.resume = resume
          s.pic = pic
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
      context = {
        "form": StudentForm(),
        "page_name": "Update Your Profile Info",
        "button_value": "Update",
        "links": ["Home"],
        "user": current_user,
      }
      return render(request, 'update.html', context)
    elif current_user.is_engineer:
      if request.method == 'POST':
        form = EngineerForm(request.POST or None)
        if form.is_valid():
          resume = form.cleaned_data['resume']
          experience = form.cleaned_data['experience']
          photo = form.cleaned_data['photo']
          contact = form.cleaned_data['contact']
          almamater = form.cleaned_data['almamater']
          bio = form.cleaned_data['bio']
          e = Engineer.objects.get(engID=request.user)
          company = Company.objects.get(id=form.cleaned_data['company'])
          if e.company is not None:
              prev_comp = e.company
              prev_comp.members.remove(current_user)
          company.members.add(current_user)
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
        "form": EngineerForm(),
        "page_name": "Update Your Profile Info",
        "button_value": "Update",
        "links": ["Home"],
        "user": current_user,
      }
      return render(request, 'update.html', context)