# -*- coding: utf-8 -*-

from django import forms

from main.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('last_modified',)
        widgets = {
            'parent_comment': forms.HiddenInput(),
            'post': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'message': forms.Textarea(attrs={'minlength': 5, 'required': 'required', 'rows': 5})
        }