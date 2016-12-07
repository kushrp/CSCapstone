"""ProjectsApp Models

Created by Harris Christiansen on 10/02/16.
"""
from django.db import models

class Project(models.Model):
    engID = models.ForeignKey("AuthenticationApp.Engineer", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=10000, null=True)
    created_at = models.DateTimeField('date created')
    updated_at = models.DateTimeField('date updated')
    company = models.ForeignKey("CompaniesApp.Company", on_delete=models.CASCADE, null=True)
    languages = models.CharField(max_length=1000, null=True)
    years = models.IntegerField(default=0);
    speciality = models.CharField(max_length=100, null=True)
    taken = models.BooleanField(default=False,)

    def __str__(self):
        return self.name