"""GroupsApp Forms

Created by Naman Patwari on 10/10/2016.
"""
from django import forms

class GroupForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30)
    description = forms.CharField(label='Description', max_length=300)
    speciality = forms.CharField(label='Group speciality', max_length=100, widget=forms.TextInput)

class MemberForm(forms.Form):
    email = forms.CharField(label='Email', required=True)