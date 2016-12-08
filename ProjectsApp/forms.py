from django import forms


class ProjectForm(forms.Form):
  name = forms.CharField(label='Name', max_length=50)
  description = forms.CharField(label='Description', max_length=300)
  created_at = forms.DateTimeField(label="Date created at")
  updated_at = forms.DateTimeField(label="Date updated at")
  languages = forms.CharField(label="Programming Languages", max_length=1000)
  speciality = forms.CharField(label="Speciality", max_length=100)
  years = forms.IntegerField(label="Years of Programming experience", min_value=0)
