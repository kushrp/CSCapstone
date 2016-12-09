"""ProjectsApp Views

Created by Harris Christiansen on 10/02/16.
"""
from django.shortcuts import render
from django.contrib import messages
from . import models
from . import forms
from django.contrib import messages
from CompaniesApp.models import Company
from AuthenticationApp.models import Engineer
from datetime import datetime
from GroupsApp.models import Group
from ProjectsApp.models import Project
from CommentsApp.models import Comment
from django.http import HttpResponseRedirect
from CommentsApp.forms import CommentForm


def getProjects(request):
  if request.user.is_authenticated():
    projects_list = list(models.Project.objects.all())
    return render(request, 'projects.html', {
      'projects': list(projects_list),
    })
  return render(request, 'autherror.html')


def getMyProjects(request):
  if request.user.is_authenticated():
    in_user_id = request.GET.get('owner')
    project_list = models.Project.objects.filter(engID=in_user_id)
    context = {
      'projects': list(project_list)
    }
    return render(request, 'projects.html', context)
  return render(request, 'autherror.html')


def getProject(request):
  if request.user.is_authenticated():
    in_name = request.GET.get('name', 'None')
    project = models.Project.objects.get(name__exact=in_name)
    bookmark_list = models.Bookmark.objects.all().filter(usr=request.user.id,project=project)
    isbookmarked = 0
    if len(bookmark_list) > 0:
      isbookmarked = 1
    comments_list = Comment.objects.filter(project_id=project.id)
    print(str(request.user.id) + " vs " + str(project.engID.engID.id))
    context = {
      'project': project,
      'currentuser': request.user,
      'comments_list': comments_list,
      'comment_form': CommentForm(),
      'isbookmarked':isbookmarked,
      'user': request.user,
      'groups_form': forms.groupSelect(user=request.user),
    }
    return render(request, 'project.html', context)
  # render error page if user is not logged in
  return render(request, 'autherror.html')


def getProjectForm(request):
  if request.user.is_authenticated():
    in_company_name = request.GET.get('name', 'None')
    if in_company_name == 'None':
      messages.warning(request, 'Please update your profile.')
      return HttpResponseRedirect('/home')
    else:
      in_company = Company.objects.get(name__exact=in_company_name)
      context = {
        'company': in_company
      }
      return render(request, 'projectform.html', {'form': forms.ProjectForm(),'company': in_company })
  # render error page if user is not logged in
  return render(request, 'autherror.html')


def getProjectFormSuccess(request):
  if request.user.is_authenticated():
    if request.method == 'POST':
      form = forms.ProjectForm(request.POST)
      if form.is_valid():
        if models.Project.objects.filter(name__exact=form.cleaned_data['name']).exists():
          return render(request, 'projectform.html', {'error': 'Error: That Project name already exists!'})

        current_eng = Engineer.objects.get(engID=request.user)
        new_project = models.Project(
          engID=current_eng,
          name=form.cleaned_data['name'],
          description=form.cleaned_data['description'],
          created_at=datetime.now(),
          updated_at=datetime.now(),
          company=current_eng.company,
          languages=form.cleaned_data['languages'],
          years=form.cleaned_data['years'],
          speciality=form.cleaned_data['speciality'],)
        new_project.save()

        context = {
          'name': form.cleaned_data['name'],
        }
        return render(request, 'projectformsuccess.html', context)
    return render(request, 'projectform.html',{
      'form': forms.ProjectForm()
    })
  # render error page if user is not logged in
  return render(request, 'autherror.html')

def getProjectUpdateFormSuccess(request):
  if request.user.is_authenticated():
    in_id = request.GET.get('id')
    if request.method == 'POST':
      form = forms.ProjectForm(request.POST)
      print(form.is_valid())
      print(form.errors)
      if form.is_valid():
        if models.Project.objects.filter(name__exact=form.cleaned_data['name']).exists():
          return render(request, 'projectupdate.html', {'error': 'Error: That Project name already exists!'})
        print(form.cleaned_data)
        in_project = Project.objects.get(id=in_id)
        if form.cleaned_data['name'] != 'None':
          in_project.name = form.cleaned_data['name']
        if form.cleaned_data['description'] != 'None':
          in_project.description = form.cleaned_data['description']
        if form.cleaned_data['languages'] != 'None':
          in_project.languages = form.cleaned_data['languages']
        if form.cleaned_data['years'] != None:
          in_project.years = form.cleaned_data['years']
        if form.cleaned_data['speciality'] != 'None':
          in_project.speciality = form.cleaned_data['speciality']

        in_project.save()

        context = {
          'name': form.cleaned_data['name'],
        }
        return render(request, 'projectformsuccess.html', context)
    return render(request, 'projectupdate.html',{
      'form': forms.ProjectForm(),
      'id' : in_id
    })
  # render error page if user is not logged in
  return render(request, 'autherror.html')

def getBookmarks(request):
  if request.user.is_authenticated():
    in_user_id = request.user.id
    bookmark_list = models.Bookmark.objects.all().filter(usr=in_user_id)
    context = {
      'bookmarks': list(bookmark_list)
    }
    return render(request, 'mybookmarks.html', context)
  return render(request, 'autherror.html')

def addBookmark(request):
  if request.user.is_authenticated():
    # context = {
    #   'user':request.user,
    #   'project': request.GET.get('id')
    # }
    current_project = Project.objects.all().get(id=request.GET.get('id'))
    print(current_project.id)
    current_user = request.user
    bookmark_new = models.Bookmark(project=current_project, usr=current_user)
    bookmark_new.save()

    return HttpResponseRedirect('/project?name=' + current_project.name)
  return render(request, 'autherror.html')

def removeBookmark(request):
  if request.user.is_authenticated():
    # context = {
    #   'user':request.user,
    #   'project': request.GET.get('id')
    # }
    current_project = Project.objects.all().get(id=request.GET.get('id'))
    current_user = request.user
    bookmark = models.Bookmark.objects.get(project=current_project, usr=current_user);
    bookmark.delete()
    return HttpResponseRedirect('/project?name=' + current_project.name)
  return render(request, 'autherror.html')

def updateProgress(request):
  if request.user.is_authenticated():
    form = forms.updateStatus(request.POST)
    if request.method == 'POST' and form.is_valid():
      print(form)
      project = Project.objects.get(id=request.GET.get('id'))
      print(project.status)
      project.status = form.data.get('status')
      project.save()
      return HttpResponseRedirect('/project?name=' + project.name)
  return render(request, 'autherror.html')


def takeProject(request):
  if request.user.is_authenticated():
    if request.method == 'POST':
      in_project = Project.objects.get(id=request.GET.get('proj'))
      form = forms.groupSelect(request.POST, user=request.user)
      print("Form valid hai ?? : " + str(form.is_valid() == True) +" "+ str(form.errors))
      if form.is_valid():
        # print("form.data cleaned data " + str(form.cleaned_data['group_ch']))
        # print("form.data data " + str(form.data.get('group_ch')))
        in_group = Group.objects.get(id=form.cleaned_data['groups'])

        if in_group.assigned == False and in_project.taken == False:
          in_group.assigned = True
          in_group.project_assgn = in_project
          in_project.taken_by = in_group
          in_project.taken = True

          in_project.save()
          in_group.save()
        else:
          messages.warning(request, 'Either the project is taken or your group is in the assigned state.')
        return HttpResponseRedirect('/project?name='+in_project.name)
    return HttpResponseRedirect('/project?name=' + in_project.name)
  # render error page if user is not logged in
  return render(request, 'autherror.html')


def ditchProject(request):
  if request.user.is_authenticated():
      in_project = Project.objects.get(id=request.GET.get('proj'))
      in_group = in_project.taken_by
      if in_group.assigned == True and in_project.taken == True:
        in_group.assigned = False
        in_group.project_assgn = None
        in_project.taken_by = None
        in_project.taken = False

        in_project.save()
        in_group.save()
      else:
        messages.warning(request, 'Either the project is not taken or your group is not in the assigned state.')
      return HttpResponseRedirect('/project?name=' + in_project.name)
  # render error page if user is not logged in
  return render(request, 'autherror.html')
