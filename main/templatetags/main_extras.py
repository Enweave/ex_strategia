# -*- coding: utf-8 -*-
from main.forms import CommentForm
from main.models import Post
from django import template

register = template.Library()


@register.inclusion_tag('post/templatetags/post_list_inner.html')
def post_list():
    return {'objects': Post.get_published()}


@register.inclusion_tag('comments/comment_form.html', takes_context=True)
def comment_form(context, user, post):
    context.update({'form': CommentForm(initial={'user': user, 'post': post})})
    return context
