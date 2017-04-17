# -*- coding: utf-8 -*-

from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from main.models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'last_modified', 'display')
    list_editable = ('display',)
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)


class CommentAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions',
        'indented_title',
        'last_modified',
        'user',
    )

    list_display_links = (
        'indented_title',
    )

    raw_id_fields = ('parent_comment',)

admin.site.register(Comment, CommentAdmin)