from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from UniversitiesApp.models import University
from CompaniesApp.models import Company

class TeacherForm(forms.Form):
    photo = forms.ImageField(label='Pic', required=False)
    university = forms.ChoiceField(label="University", widget=forms.Select(),
                                   choices=tuple((u.id, u.name) for u in University.objects.all()), required=False)
    department = forms.CharField(label='Department',widget=forms.TextInput, required=False)
    almamater = forms.CharField(label="Alma Mater", widget=forms.TextInput, required=False)
    contact = forms.IntegerField(label='Phone', widget=forms.NumberInput, required=False)

    def __init__(self, *args, **kwargs):
      super(TeacherForm, self).__init__(*args, **kwargs)
      self.fields['university'] = forms.ChoiceField(label="University", widget=forms.Select(),
                                   choices=tuple((u.id, u.name) for u in University.objects.all()), required=False)
class StudentForm(forms.Form):
    university = forms.ChoiceField(label="University", widget=forms.Select(),
                                   choices=tuple((u.id, u.name) for u in University.objects.all()), required=False)
    major = forms.CharField(label='Major', widget=forms.TextInput, required=False)
    skills = forms.CharField(label='Skills (comma separated list)', widget=forms.TextInput, required=False)
    resume = forms.FileField(label='Resume', widget=forms.FileInput, required=False)
    experience = forms.IntegerField(label='Experience', widget=forms.NumberInput, required=False)
    grades = ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Grad', 'Doc']
    year = forms.ChoiceField(label='Year', widget=forms.Select(), required=False, choices=tuple((u, u) for u in grades))
    photo = forms.ImageField(label='Pic', required=False)
    def __init__(self, *args, **kwargs):
      super(StudentForm, self).__init__(*args, **kwargs)
      self.fields['university'] = forms.ChoiceField(label="University", widget=forms.Select(),
                                   choices=tuple((u.id, u.name) for u in University.objects.all()), required=False)

class EngineerForm(forms.Form):
    company = forms.ChoiceField(label="Company", widget=forms.Select(),
                                   choices=tuple((c.id, c.name) for c in Company.objects.all()), required=True)
    resume = forms.FileField(label='Resume', widget=forms.FileInput, required=False)
    experience = forms.IntegerField(label='Experience', widget=forms.NumberInput, required=False)
    photo = forms.ImageField(label='Pic', required=False)
    contact = forms.IntegerField(label="Phone", widget=forms.NumberInput,required=False)
    bio = forms.CharField(label="bio", widget=forms.TextInput, required=False)
    almamater = forms.CharField(label="almamater", widget=forms.TextInput,required=False)
    def __init__(self, *args, **kwargs):
      super(EngineerForm, self).__init__(*args, **kwargs)
      self.fields['company'] = forms.ChoiceField(label="Company", widget=forms.Select(),
                                   choices=tuple((c.id, c.name) for c in Company.objects.all()), required=False)