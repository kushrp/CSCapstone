"""ProjectsApp Views

Created by Harris Christiansen on 10/02/16.
"""
from django.shortcuts import render
from . import models
from . import forms
from CompaniesApp.models import Company
from AuthenticationApp.models import Engineer
from datetime import datetime


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
    project_list = models.Project.objects.all().filter(engID=in_user_id)
    context = {
      'projects': list(project_list)
    }
    return render(request, 'groups.html', context)
  return render(request, 'autherror.html')


def getProject(request):
  if request.user.is_authenticated():
    in_name = request.GET.get('name', 'None')
    project = models.Project.objects.get(name__exact=in_name)
    context = {
      'project': project,
    }
    return render(request, 'project.html', context)
  # render error page if user is not logged in
  return render(request, 'autherror.html')


def getProjectForm(request):
  if request.user.is_authenticated():
    return render(request, 'projectform.html', {
      'form': forms.ProjectForm()
    })
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
