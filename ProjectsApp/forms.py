from django import forms
from GroupsApp.models import Group

class ProjectForm(forms.Form):
  name = forms.CharField(label='Name', max_length=50)
  description = forms.CharField(label='Description', max_length=300)
  created_at = forms.DateTimeField(label="Date created at")
  updated_at = forms.DateTimeField(label="Date updated at")
  languages = forms.CharField(label="Programming Languages", max_length=1000)
  speciality = forms.CharField(label="Speciality", max_length=100)
  years = forms.IntegerField(label="Years of Programming experience", min_value=0)

class updateStatus(forms.Form):
  status = forms.IntegerField(label="status", min_value=0, max_value=100)

class groupSelect(forms.Form):
  groups = forms.ChoiceField(label="Group", widget=forms.Select(), required=True)

  def __init__(self, *args, **kwargs):
    myuser = kwargs.pop("user")
    all_groups = list(Group.objects.all())
    tup = tuple((group.id, group.name) for group in all_groups if myuser in list(group.members.all()))
    super(groupSelect, self).__init__(*args, **kwargs)
    self.fields['groups'] = forms.ChoiceField(label="Group", widget=forms.Select(),
                                                  choices=tup,
                                                  required=False)