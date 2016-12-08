"""ProjectsApp URL Configuration

Created by Harris Christiansen on 10/02/16.
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^project/all$', views.getProjects, name='Projects'),
    url(r'^project$', views.getProject, name='Project'),
    url(r'^project/form$', views.getProjectForm, name="Project Form"),
    url(r'^project/getMyProjects$', views.getMyProjects, name="GetMyProjects"),
    url(r'^project/formsuccess$', views.getProjectFormSuccess, name="Project Form Success"),
    url(r'^project/mybookmarks$', views.getBookmarks, name="My Bookmarks"),
    url(r'^project/addbookmark$', views.addBookmark, name="Add Bookmark"),
    url(r'^project/bookmarksuccess$', views.getProjectFormSuccess, name="Project Form Success"),
]