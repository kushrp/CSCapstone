from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from UniversitiesApp import models

class TeacherForm(forms.Form):
    image = forms.ImageField(label='Pic', widget=forms.FileInput, required=False)

    universities_list = models.University.objects.all()
    uni = []
    for univ in universities_list:
        list_uni = []
        list_uni.append(univ.id)
        list_uni.append(univ.name)
        uni.append(tuple(list_uni))
    university = forms.ChoiceField(label="Select University", widget=forms.Select(), choices=uni, required=True)

    department = forms.CharField(label='Department',widget=forms.TextInput, required=True)
    almamater = forms.CharField(label="Alma Mater", widget=forms.TextInput, required=True)
    contact = forms.IntegerField(label='Phone', widget=forms.NumberInput, required=True)

class CoursesForm(forms.Form):
    tag = forms.CharField(label='Tag', widget=forms.TextInput, required=True)
    name = forms.CharField(label='Course Name', widget=forms.TextInput, required=True)
    description = forms.CharField(label='Description', widget=forms.TextInput, required=True)

class StudentForm(forms.Form):
    major = forms.CharField(label='Major', widget=forms.TextInput, required=True)
    skills = forms.CharField(label='Skills (comma separated list)', widget=forms.TextInput, required=True)
    resume = forms.FileField(label='Resume', widget=forms.FileInput, required=True)
    experience = forms.IntegerField(label='Experience', widget=forms.NumberInput)
    year = forms.IntegerField(label='Year', widget=forms.NumberInput)