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
	projects_list = models.Project.objects.all()
	return render(request, 'projects.html', {
        'projects': projects_list,
    })

def getProject(request):
	return render(request, 'project.html')

def getProjectForm(request):
	if request.user.is_authenticated():
		return render(request, 'projectform.html')
	return render(request, 'autherror.html')

def getProjectFormSuccess(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = forms.ProjectForm(request.POST)
			if form.is_valid():
				if models.Project.objects.filter(name__exact=form.cleaned_data['name']).exists():
					return render(request, 'projectform.html', {'error' : 'Error: That Project name already exists!'})
				new_project = models.Project(
					    engID = Engineer.engID,
    					name = form.cleaned_data['name'],
    					description = form.cleaned_data['description'],
    					created_at = datetime.now(),
   						updated_at = datetime.now(),
    					company = Company.name,
    					languages = form.cleaned_data['languages'],
    					years = form.cleaned_data['years'],
    					speciality =  form.cleaned_data['speciality'])
				new_project.save()
				context = {
                    'name' : form.cleaned_data['name'],
                }
				return render(request, 'projectformsuccess.html', context)
		else:
			form = forms.ProjectForm()
		return render(request, 'projectform.html')
	# render error page if user is not logged in
	return render(request, 'autherror.html')
