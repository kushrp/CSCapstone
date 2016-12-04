from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from UniversitiesApp.models import University

class TeacherForm(forms.Form):
    pic = forms.ImageField(label='Pic', widget=forms.FileInput, required=False)
    universities_list = list(University.objects.all())
    uni = tuple((u, u.name) for u in universities_list)
    university = forms.ChoiceField(label="University", widget=forms.Select(), choices=uni, required=True)
    department = forms.CharField(label='Department',widget=forms.TextInput, required=True)
    almamater = forms.CharField(label="Alma Mater", widget=forms.TextInput, required=True)
    contact = forms.IntegerField(label='Phone', widget=forms.NumberInput, required=True)


    def __init__(self, user, *args, **kwargs):
      super(TeacherForm, self).__init__(*args, **kwargs)
      universities_list = list(University.objects.all())
      self.fields['university'] = forms.ChoiceField(label="University",
        choices=tuple((u.id, u.name) for u in universities_list),widget=forms.Select(), required=True)

class StudentForm(forms.Form):
    universities_list = list(University.objects.all())
    uni = tuple((u, u.name) for u in universities_list)
    university = forms.ChoiceField(label="University", widget=forms.Select(), choices=uni, required=True)

    major = forms.CharField(label='Major', widget=forms.TextInput, required=True)
    skills = forms.CharField(label='Skills (comma separated list)', widget=forms.TextInput, required=True)
    resume = forms.FileField(label='Resume', widget=forms.FileInput, required=False)
    experience = forms.IntegerField(label='Experience', widget=forms.NumberInput)

    grades = ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Grad', 'Doc']
    choices_in = tuple((u, u) for u in grades)
    year = forms.ChoiceField(label='Year', widget=forms.Select(), required=True, choices=choices_in)

    def __init__(self, user, *args, **kwargs):
      super(StudentForm, self).__init__(*args, **kwargs)
      universities_list = list(University.objects.all())
      self.fields['university'] = forms.ChoiceField(label="University",
        choices=tuple((u.id, u.name) for u in universities_list),widget=forms.Select(), required=True)