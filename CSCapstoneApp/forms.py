from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from UniversitiesApp.models import University

class TeacherForm(forms.Form):
    photo = forms.ImageField(label='Pic', required=False)
    university = forms.ChoiceField(label="University", widget=forms.Select(),
                                   choices=tuple((u.id, u.name) for u in University.objects.all()), required=True)
    department = forms.CharField(label='Department',widget=forms.TextInput, required=True)
    almamater = forms.CharField(label="Alma Mater", widget=forms.TextInput, required=True)
    contact = forms.IntegerField(label='Phone', widget=forms.NumberInput, required=True)

    def __init__(self, *args, **kwargs):
      super(TeacherForm, self).__init__(*args, **kwargs)
      self.fields['university'] = forms.ChoiceField(label="University", widget=forms.Select(),
                                   choices=tuple((u.id, u.name) for u in University.objects.all()), required=True)
class StudentForm(forms.Form):
    university = forms.ChoiceField(label="University", widget=forms.Select(),
                                   choices=tuple((u.id, u.name) for u in University.objects.all()), required=True)
    major = forms.CharField(label='Major', widget=forms.TextInput, required=True)
    skills = forms.CharField(label='Skills (comma separated list)', widget=forms.TextInput, required=True)
    resume = forms.FileField(label='Resume', widget=forms.FileInput, required=False)
    experience = forms.IntegerField(label='Experience', widget=forms.NumberInput)
    grades = ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Grad', 'Doc']
    year = forms.ChoiceField(label='Year', widget=forms.Select(), required=True, choices=tuple((u, u) for u in grades))
    photo = forms.ImageField(label='Pic', required=False)
    def __init__(self, *args, **kwargs):
      super(StudentForm, self).__init__(*args, **kwargs)
      self.fields['university'] = forms.ChoiceField(label="University", widget=forms.Select(),
                                   choices=tuple((u.id, u.name) for u in University.objects.all()), required=True)