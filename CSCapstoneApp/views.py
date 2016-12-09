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
    profiler_id = request.GET.get('id')

    if profiler_id == None:
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
      if myuser.is_professor == True:
        type = "Teacher"
        a = Teacher.objects.filter(teacher=myuser)[0]
        class_list = list(Course.objects.filter(teacher=a))
      elif myuser.is_student == True:
        type = "Student"
        a = Student.objects.get(user_id=myuser)
        for course in list(Course.objects.all()):
          if myuser in list(course.members.all()):
            course_list.append(course)
        for group in list(Group.objects.all()):
          if myuser in list(group.members.all()):
            groups_list.append(group)
      elif myuser.is_engineer == True:
        type = "Engineer"
        a = Engineer.objects.get(engID=myuser)
        for project in list(Project.objects.all()):
          if myuser.id == project.engID:
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
            print(form.cleaned_data)
            t = Teacher.objects.get(teacher=request.user)
            # print(form)

            university_id = form.cleaned_data['university']
            university = University.objects.get(id=university_id)
            t.university = university
            if t.university is not None:
              prev_uni = t.university
              prev_uni.members.remove(current_user)
            university.members.add(current_user)



            if form.cleaned_data['department'] != '':
              department = form.cleaned_data['department']
              t.department = department

            if form.cleaned_data['contact'] != None:
              contact = form.cleaned_data['contact']
              t.contact = contact

            if form.cleaned_data['almamater'] != '':
              almamater = form.cleaned_data['almamater']
              t.almamater = almamater
            # pic = request.FILES['photo']





            # t.pic = pic
            t.save()
            messages.success(request, 'Success, your profile was saved!')
            return HttpResponseRedirect('/home')
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
          s = Student.objects.get(user=request.user)
          print(form.cleaned_data)
          university_id = form.data['university']
          university = University.objects.get(id=university_id)
          if s.university is not None:
            prev_uni = s.university
            prev_uni.members.remove(current_user)
          university.members.add(current_user)
          s.university = university

          if form.data['major'] != '':
            major = form.cleaned_data['major']
            s.major = major

          if form.data['skills'] != '':
            skills = form.cleaned_data['skills']
            s.skills = skills

          # resume = form.data['resume']
          if form.cleaned_data['experience'] != None:
            experience = form.cleaned_data['experience']
            s.experience = experience

          if form.cleaned_data['year'] != None:
            year = form.cleaned_data['year']
            s.year = year

          # pic = request.FILES['photo']



          # s.resume = resume
          # s.pic = pic



          s.save()

          messages.success(request, 'Success, your profile was saved!')
          return HttpResponseRedirect('/home')
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
          print(form.cleaned_data)
          # resume = form.cleaned_data['resume']
          e = Engineer.objects.get(engID=request.user)

          if form.cleaned_data['experience'] != None:
            experience = form.cleaned_data['experience']
            e.experience = experience

          if form.cleaned_data['photo'] != None:
            photo = form.cleaned_data['photo']

          if form.cleaned_data['contact'] != None:
            contact = form.cleaned_data['contact']
            e.contact = contact

          if form.cleaned_data['almamater'] != '':
            almamater = form.cleaned_data['almamater']
            e.almamater = almamater

          if form.cleaned_data['bio'] != '':
            bio = form.cleaned_data['bio']
            e.bio = bio


          company = Company.objects.get(id=form.cleaned_data['company'])
          if e.company is not None:
              prev_comp = e.company
              prev_comp.members.remove(current_user)
          company.members.add(current_user)
          e.company = company

          # e.resume = resume

          # e.photo = photo



          e.save()

          messages.success(request, 'Success, your profile was saved!')
          return HttpResponseRedirect('/home')
      context = {
        "form": EngineerForm(),
        "page_name": "Update Your Profile Info",
        "button_value": "Update",
        "links": ["Home"],
        "user": current_user,
      }
      return render(request, 'update.html', context)