"""AuthenticationApp Views

Created by Naman Patwari on 10/4/2016.
"""

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages

from .forms import LoginForm, RegisterForm, UpdateForm
from .models import MyUser, Student, Teacher, Engineer


# Auth Views

def auth_login(request):
  form = LoginForm(request.POST or None)
  next_url = request.GET.get('next')
  if next_url is None:
    next_url = "/home"
  if form.is_valid():
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    user = authenticate(email=email, password=password)
    if user is not None:
      messages.success(request, 'Success! Welcome, ' + (user.first_name or ""))
      login(request, user)
      return HttpResponseRedirect(next_url)
    else:
      messages.warning(request, 'Invalid username or password.')

  context = {
    "form": form,
    "page_name": "Login",
    "button_value": "Login",
    "links": ["register"],
  }
  return render(request, 'auth_form.html', context)


def auth_logout(request):
  logout(request)
  messages.success(request, 'Success, you are now logged out')
  return render(request, 'index.html')


def auth_register(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect("/home")

  form = RegisterForm(request.POST or None)

  if form.is_valid():
    is_student = False
    is_prof = False
    is_engine = False
    print(form.cleaned_data['type_acc'] )
    if form.cleaned_data['type_acc'] == 'S':
      is_student = True
    elif form.cleaned_data['type_acc'] == 'T':
      is_prof = True
    elif form.cleaned_data['type_acc'] == 'E':
      is_engine = True

    new_user = MyUser.objects.create_user(email=form.cleaned_data['email'],
                                          password=form.cleaned_data["password2"],
                                          first_name=form.cleaned_data['firstname'],
                                          last_name=form.cleaned_data['lastname'], is_student=is_student,
                                          is_professor=is_prof, is_engineer=is_engine)
    new_user.save()

    if is_student:
      new_student = Student(user=new_user)
      new_student.save()
    elif is_engine:
      new_engine = Engineer(engID=new_user)
      new_engine.save()
    else:
      new_teacher = Teacher(teacher=new_user)
      new_teacher.save()

    login(request, new_user)
    messages.success(request, 'Success! Your account was created.')
    return HttpResponseRedirect("/home")

  context = {
    "form": form,
    "page_name": "Register",
    "button_value": "Register",
    "links": ["login"],
  }
  return render(request, 'auth_form.html', context)


@login_required
def update_profile(request):
  form = UpdateForm(request.POST or None, instance=request.user)
  if form.is_valid():
    form.save()
    messages.success(request, 'Success, your profile was saved!')

  context = {
    "form": form,
    "page_name": "Update",
    "button_value": "Update",
    "links": ["logout"],
  }
  return render(request, 'auth_form.html', context)
