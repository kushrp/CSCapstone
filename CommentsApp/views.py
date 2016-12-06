from django.shortcuts import render
from CommentsApp.models import Comment, Sub_Comment
from . import models

from . import forms


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
        if form.is_valid():
            #new comment creation
            new_comment = models.Comment(comment=form.cleaned_data['comment'])
            new_comment.save()

            #comments list
            comments_list = models.Comment.objects.all()
            context = {
                'comments' : list(comments_list),
                'form' : forms.CommentForm(),
            }
            return render(request, 'commentForm.html', context)

    return render(request, 'commentForm.html', {
        'comments': list(models.Comment.objects.all()),
        'form': forms.CommentForm(),
    })

def addSubComment(request):
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        comment_id = request.GET.get('id')
        if form.is_valid():
            comment = Comment.objects.get(id=comment_id)

            #creating the subcomment
            new_sub_comment = models.Sub_Comment(data=form.cleaned_data['comment'])
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