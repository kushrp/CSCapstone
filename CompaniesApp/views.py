"""
CompaniesApp Views

Created by Jacob Dunbar on 10/2/2016.
"""
from django.shortcuts import render

from . import models
from . import forms
from AuthenticationApp.models import Teacher, Student, Engineer
from ProjectsApp.models import Project

def getCompanies(request):
    if request.user.is_authenticated():
        companies_list = models.Company.objects.all()
        context = {
            'companies' : companies_list,
        }
        return render(request, 'companies.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getCompany(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_company = models.Company.objects.get(name__exact=in_name)
        is_member = in_company.members.filter(email__exact=request.user.email)
        is_engineer = False
        if request.user.is_engineer:
            is_engineer = True
        projects = Project.objects.filter(company=in_company)
        context = {
            'company' : in_company,
            'userIsMember': is_member,
            'engine':is_engineer,
            'projects': projects,
        }
        return render(request, 'company.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getCompanyForm(request):
    if request.user.is_authenticated():
        return render(request, 'companyform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getCompanyFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.CompanyForm(request.POST, request.FILES)
            if form.is_valid():
                if models.Company.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'companyform.html', {'error' : 'Error: That company name already exists!'})
                new_company = models.Company(name=form.cleaned_data['name'], 
                                             photo=request.FILES['photo'],  
                                             description=form.cleaned_data['description'],
                                             website=form.cleaned_data['website'])
                new_company.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'companyformsuccess.html', context)
            else:
                return render(request, 'companyform.html', {'error' : 'Error: Photo upload failed!'})
        else:
            form = forms.CompanyForm()
        return render(request, 'companyform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinCompany(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_company = models.Company.objects.get(name__exact=in_name)
        in_company.members.add(request.user)
        in_company.save()
        cureng = Engineer.objects.get(engID=request.user.id)
        prev_comp = cureng.company
        if prev_comp is not None:
            prev_comp.members.remove(request.user)
        cureng.company = in_company
        cureng.save()
        context = {
            'company' : in_company,
            'userIsMember': True,
        }
        return render(request, 'company.html', context)
    return render(request, 'autherror.html')
    
def unjoinCompany(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_company = models.Company.objects.get(name__exact=in_name)
        in_company.members.remove(request.user)
        in_company.save()
        cureng = Engineer.objects.get(engID=request.user.id)
        # prev_comp = cureng.company
        # if prev_comp is not None:
        #     prev_comp.members.remove(request.user)
        cureng.company = None
        cureng.save()
        context = {
            'company' : in_company,
            'userIsMember': False,
        }
        return render(request, 'company.html', context)
    return render(request, 'autherror.html')
    