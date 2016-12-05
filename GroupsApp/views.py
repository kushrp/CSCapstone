"""GroupsApp Views
Created by Naman Patwari on 10/10/2016.
"""
from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import models
from . import forms

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
        form = forms.MemberForm()
        context = {
            'group' : in_group,
            'userIsMember': is_member,
            'member_form': form,
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
                group.save()
                context = {
                    'group': group,
                    'userIsMember': is_member,
                    'member_form': forms.MemberForm(),
                }
                return render(request, 'group.html', context)
        else:
            return HttpResponseRedirect('/home')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupForm(request):
    if request.user.is_authenticated():
        return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.GroupForm(request.POST)
            if form.is_valid():
                if models.Group.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'groupform.html', {'error' : 'Error: That Group name already exists!'})
                new_group = models.Group(name=form.cleaned_data['name'], description=form.cleaned_data['description'], owner=request.user)
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
        context = {
            'group' : in_group,
            'userIsMember': True,
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
        context = {
            'group' : in_group,
            'userIsMember': False,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')
    