"""GroupsApp Models

Created by Naman Patwari on 10/10/2016.
"""
from django.db import models
from AuthenticationApp.models import MyUser
from ProjectsApp.models import Project

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    members = models.ManyToManyField(MyUser)
    owner = models.ForeignKey('AuthenticationApp.MyUser', on_delete=models.CASCADE, null=True, related_name='maalik')
    project = models.OneToOneField(Project, null=True)
    match_factor = models.IntegerField(default=0)
    assigned = models.BooleanField(default=False,)
    speciality = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name