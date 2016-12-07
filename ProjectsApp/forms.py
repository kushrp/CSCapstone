from django import forms


class ProjectForm(forms.Form):
  name = forms.CharField(label='Name', max_length=50, widget=forms.TextInput)
  description = forms.CharField(label='Description', max_length=300, widget=forms.TextInput)
  created_at = forms.DateTimeField(label="Date created at", widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
  updated_at = forms.DateTimeField(label="Date updated at", widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
  languages = forms.CharField(label="Programming Languages", max_length=1000,widget=forms.TextInput)
  speciality = forms.CharField(label="Speciality", max_length=100,widget=forms.TextInput)
  years = forms.IntegerField(label="Experience of Programming experience",widget=forms.NumberInput)
