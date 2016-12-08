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
from AuthenticationApp.models import MyUser
from datetime import datetime
from GroupsApp.models import Group
from ProjectsApp.models import Project

from django.http import HttpResponseRedirect


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
    context = {
      'project': project,
      'currentuser': request.user,
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
      in_company = models.Company.objects.get(name__exact=in_company_name)
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


<<<<<<< HEAD
def getBookmarks(request):
  if request.user.is_authenticated():
    in_user_id = request.user.id
    print(in_user_id)
    bookmark_list = models.Bookmark.objects.all().filter(usr=in_user_id)
    context = {
      'bookmarks': list(bookmark_list)
    }
    return render(request, 'mybookmarks.html', context)
  return render(request, 'autherror.html')

=======
def takeProject(request):
  if request.user.is_authenticated():
    group_id = request.GET.get('id')
    project_id = request.GET.get('proj')
    in_group = Group.objects.get(id=group_id)
    in_project = Project.objects.get(id=project_id)
    if in_group.assigned == False and in_project.taken == False:
      in_group.assigned = True
      in_project.taken_by = in_group
      in_project.taken = True

      in_project.save()
      in_group.save()
    else:
      messages.warning(request, 'Either the project is taken or your group is in the assigned state.')
    return HttpResponseRedirect('/project?name='+in_project.name)
  # render error page if user is not logged in
  return render(request, 'autherror.html')



def ditchProject(request):
    if request.user.is_authenticated():
      group_id = request.GET.get('id')
      project_id = request.GET.get('proj')
      in_group = Group.objects.get(id=group_id)
      in_project = Project.objects.get(id=project_id)

      if in_group.assigned == True and in_project.taken == True:
        in_group.assigned = False
        in_project.taken_by = None
        in_project.taken = False

        in_project.save()
        in_group.save()
      else:
        messages.warning(request, 'Either the project is not taken or your group is not in the assigned state.')
      return HttpResponseRedirect('/project?name=' + in_project.name)
    # render error page if user is not logged in
    return render(request, 'autherror.html')
>>>>>>> eceaa11ee4dc82edd84a49ee51360d23788acff0
