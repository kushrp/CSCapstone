"""GroupsApp Views
Created by Naman Patwari on 10/10/2016.
"""
from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import models
from . import forms
from CommentsApp.forms import CommentForm
from CommentsApp.models import Comment,Sub_Comment
from ProjectsApp.models import Project
from GroupsApp.models import Group
from AuthenticationApp.models import Student

def getGroups(request):
    if request.user.is_authenticated():
        groups_list = models.Group.objects.all()
        context = {
            'groups' : list(groups_list),
        }
        return render(request, 'groups.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getMyGroups(request):
  if request.user.is_authenticated():
    in_user_id = request.GET.get('owner')
    group_list = models.Group.objects.all().filter(owner=in_user_id)
    context = {
      'groups' : list(group_list)
    }
    return render(request, 'groups.html', context)
  return render(request, 'autherror.html')

def getGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_member = in_group.members.filter(email__exact=request.user.email)
        members = in_group.members.values_list()
        comments_list = Comment.objects.filter(group_id=in_group.id)
        print(members)
        form = forms.MemberForm()
        matching_proj = matching_algorithm(in_group.id)
        context = {
            'group' : in_group,
            'userIsMember': is_member,
            'member_form': form,
            'comment_form': CommentForm(),
            'comments_list': comments_list,
            'matching_projs': matching_proj,
            'user': request.user,
        }
        return render(request, 'group.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def addMember(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.MemberForm(request.POST, 'None')
            if form.is_valid():
                email = form.cleaned_data['email']
                group_id = request.GET.get('id')
                myuser = models.MyUser.objects.get(email=email)
                group = models.Group.objects.get(id=group_id)
                group.members.add(myuser)
                is_member = group.members.filter(email__exact=request.user.email)
                comments_list = Comment.objects.filter(group_id=group.id)
                group.save()
                matching_proj = matching_algorithm(group.id)
                context = {
                    'group': group,
                    'userIsMember': is_member,
                    'member_form': forms.MemberForm(),
                    'comment_form': CommentForm(),
                    'comments_list': comments_list,
                    'matching_projs': matching_proj,
                    'user': request.user,
                }
                return render(request, 'group.html', context)
        else:
            return HttpResponseRedirect('/home')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupForm(request):
    if request.user.is_authenticated():
        return render(request, 'groupform.html', {
          'form': forms.GroupForm(),
        })
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.GroupForm(request.POST)
            if form.is_valid():
                if models.Group.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'groupform.html', {'error' : 'Error: That Group name already exists!'})
                new_group = models.Group(name=form.cleaned_data['name'], description=form.cleaned_data['description'],
                                         owner=request.user,speciality=form.cleaned_data['speciality'])
                new_group.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'groupformsuccess.html', context)
        else:
            form = forms.GroupForm()
        return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.add(request.user)
        in_group.save();
        request.user.group_set.add(in_group)
        request.user.save()
        comments_list = Comment.objects.filter(group_id=in_group.id)
        context = {
            'group' : in_group,
            'userIsMember': True,
            'comment_form': CommentForm(),
            'comments_list': comments_list,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')
    
def unjoinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.remove(request.user)
        in_group.save();
        request.user.group_set.remove(in_group)
        request.user.save()
        matching_proj = matching_algorithm(in_group.id)
        comments_list = Comment.objects.filter(group_id=in_group.id)
        context = {
            'group' : in_group,
            'userIsMember': False,
            'comment_form': CommentForm(),
            'comments_list': comments_list,
            'matching_projs': matching_proj,
            'user': request.user,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')

def matching_algorithm(group_id):
    project_list = list(Project.objects.all())
    ret = []

    combined_skills = []
    average_experience = 0

    in_group = Group.objects.get(id=group_id)
    total_number_students = len(in_group.members.all())
    print("Total number of students " + str(total_number_students))

    for member in in_group.members.all():
      s = Student.objects.get(user=member)
      skills_list = s.skills.split(",")
      average_experience += s.experience
      for skill in skills_list:
        combined_skills.append(skill)
    if total_number_students != 0:
      average_experience = average_experience/total_number_students
    else:
      average_experience = 0
    combined_skills = list(set(combined_skills))
    print("Combined skills " + str(combined_skills))
    print("Average experience " + str(average_experience))

    for project in project_list:
      skill_match = 0
      language_reqs = project.languages.split(",")
      print("Projects " + str(project.name))
      for skill in language_reqs:
        if skill in combined_skills:
          skill_match += 1
      print("Number of skills matched " + str(skill_match))
      print("Languages required " + str(language_reqs))
      print("Experience required " + str(project.years))
      print("Speciality of the group " + str(in_group.speciality) + " vs what is needed " + project.speciality)
      if skill_match >= len(language_reqs) and average_experience >= project.years and in_group.speciality == project.speciality:
        ret.append(project)
    print("Matched projects : " + str(ret))
    return ret