from __future__ import unicode_literals

from django.db import models
from GroupsApp.models import Group
from ProjectsApp.models import Project
from AuthenticationApp.models import MyUser

class Sub_Comment(models.Model):
    time = models.DateTimeField(auto_now=True)
    data = models.CharField(max_length=500, null=True)
    owner = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE)

    def __str__(self):
        # toString() method
        return str(self.comment_id) + ", "+ str(self.time) + ", " + self.comment


class Comment(models.Model):
    time = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=500)
    subs = models.ManyToManyField(Sub_Comment)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE)

    def __str__(self):
        # toString() method
        return str(self.time) + ", " + self.comment