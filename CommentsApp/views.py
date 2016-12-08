from django.shortcuts import render
from CommentsApp.models import Comment, Sub_Comment
from django.http import HttpResponseRedirect
from . import models

from . import forms
from GroupsApp.models import Group
from ProjectsApp.models import Project


# def getComments(request):
#     return render(request, 'comments.html')


def getCommentForm(request):
    comments_list = list(models.Comment.objects.all())
    context = {
        'comments': list(comments_list),
        'form': forms.CommentForm()
    }
    return render(request, 'commentForm.html', context)

def addComment(request):
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        group_id = request.GET.get('group')
        project_id = request.GET.get('project')
        print("Group : " + str(group_id) + " ," + " Projects: "+ str(project_id))
        if form.is_valid() and group_id == None and project_id == None:
            #new comment creation
            new_comment = models.Comment(comment=form.cleaned_data['comment'], owner=request.user)
            new_comment.save()

            #comments list
            comments_list = models.Comment.objects.all()
            context = {
                'comments' : list(comments_list),
                'form' : forms.CommentForm(),
            }
            return render(request, 'commentForm.html', context)
        elif form.is_valid() and project_id == None:
            currGroup = Group.objects.get(id=group_id)
            new_comment = models.Comment(comment=form.cleaned_data['comment'], group_id=currGroup,owner=request.user)
            new_comment.save()

            return HttpResponseRedirect('group?name='+currGroup.name)
        elif form.is_valid() and group_id == None:
            currProj = Project.objects.get(id=project_id)
            new_comment = models.Comment(comment=form.cleaned_data['comment'], project_id=currProj,owner=request.user)
            new_comment.save()

            return HttpResponseRedirect('project?name=' + currProj.name)

    return render(request, 'commentForm.html', {
        'comments': list(models.Comment.objects.all()),
        'form': forms.CommentForm(),
    })

def addSubComment(request):
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        comment_id = request.GET.get('id')
        group_id = request.GET.get('group')
        project_id = request.GET.get('project')
        print("Group : " + str(group_id) + " ," + " Projects: " + str(project_id) + ", id: " + str(comment_id))
        if form.is_valid() and group_id == None and project_id == None:
            comment = Comment.objects.get(id=comment_id)

            #creating the subcomment
            new_sub_comment = models.Sub_Comment(data=form.cleaned_data['comment'], owner=request.user)
            new_sub_comment.save()

            #adding the sub comment to the comment
            comment.subs.add(new_sub_comment)
            comment.save()

            #default context
            context = {
                'comments' : list(Comment.objects.all()),
                'form': forms.CommentForm(),
            }
            return render(request, 'commentForm.html', context)
        elif form.is_valid() and project_id == None:
            comment = Comment.objects.get(id=comment_id)

            currGroup = Group.objects.get(id=group_id)
            # creating the subcomment
            new_sub_comment = models.Sub_Comment(data=form.cleaned_data['comment'], owner=request.user)
            new_sub_comment.save()

            # adding the sub comment to the comment
            comment.subs.add(new_sub_comment)
            comment.save()

            return HttpResponseRedirect('group?name=' + currGroup.name)
        elif form.is_valid() and group_id == None:
            comment = Comment.objects.get(id=comment_id)

            currProj = Project.objects.get(id=project_id)
            # creating the subcomment
            new_sub_comment = models.Sub_Comment(data=form.cleaned_data['comment'], owner=request.user)
            new_sub_comment.save()

            # adding the sub comment to the comment
            comment.subs.add(new_sub_comment)
            comment.save()

            return HttpResponseRedirect('project?name=' + currProj.name)
    # default context
    return render(request, 'commentForm.html', {
        'comments': list(Comment.objects.all()),
        'form': forms.CommentForm(),
    })

def getComments(request):
    comments_list = models.Comment.objects.all()
    context = {
        'comments' : comments_list,
    }
    return render(request, 'comments.html', context)