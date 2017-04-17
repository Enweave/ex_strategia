# -*- coding: utf-8 -*-
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string

from main.forms import CommentForm
from main.models import Post, Comment


def post_list(request):
    return render(request, 'post/post_list.html', {
        'objects': Post.get_published(),
        'breadcrumbs': Post.get_breadcrumbs_base(),
        'page_title': Post.LIST_VIEW_HEADING
    }
                  )


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'post/post_detail.html', {
        'object': post,
        'breadcrumbs': post.get_breadcrumbs()
        }
    )


def load_comments(request):
    if request.is_ajax():
        comment = Comment.objects.get(id=request.GET.get('comment_id'))
        return HttpResponse(json.dumps(
            {
                'htmlData': render_to_string('comments/post_comments.html',
                {
                    'nodes': comment.get_children(),
                    'can_post': request.user.is_authenticated
                }
            )}
        ), content_type="application/json")
    return HttpResponseForbidden()


@login_required
def post_comment(request):
    if request.POST and request.is_ajax():
        json_context = {
            'success': False,
            'form_errors': []
        }

        form = CommentForm(request.POST)
        comment = form.save()
        if form.is_valid():
            json_context['success'] = 'Комментарий успешно добавлен!'
            json_context['commentHtml'] = render_to_string('comments/post_comments.html', {
                'nodes': [comment],
                'can_post': True
            }
                                                           )
        else:
            json_context['form_errors'] = form.errors
        return HttpResponse(json.dumps(json_context), content_type="application/json")
    return HttpResponseForbidden()
