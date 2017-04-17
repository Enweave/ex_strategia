# -*- coding: utf-8 -*-
import itertools
import time

from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models.signals import post_save, pre_delete, post_delete
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager
from mptt.models import MPTTModel
from email.utils import formatdate
from main.mixins.models import SitePageModel
from django.utils.translation import ugettext_lazy as _


class Post(SitePageModel):
    LIST_VIEW_HEADING = _(u'All posts')
    comments_count = models.IntegerField(_(u'Comments count'), default=0)

    class Meta:
        verbose_name = _(u'Post')
        verbose_name_plural = _(u'Posts')
        ordering = ('last_modified',)

    def get_comments(self, root=None):
        if root:
            return root.get_children()
        else:
            return Comment.tree.filter(post=self, level__lte=2)

    def get_comments_count(self):
        return self.comments_count

    @classmethod
    def get_breadcrumbs_base(cls):
        return [
            {
                'title': cls.LIST_VIEW_HEADING,
                'url': reverse('post-list')
            },
        ]

    def get_breadcrumbs(self):
        return itertools.chain(
            self.get_breadcrumbs_base(),
            [
                {
                    'title': self.title,
                    'url': self.get_absolute_url()
                }
            ]
        )

    @models.permalink
    def get_absolute_url(self):
        return 'post-detail', (), {'slug': self.slug}


class Comment(MPTTModel):
    user = models.ForeignKey('auth.User', verbose_name=_(u'User'))
    post = models.ForeignKey('Post', verbose_name=_(u'Post'))

    message = models.TextField(
        verbose_name=_(u'Message'),
        max_length=1000,
        validators=[MinLengthValidator(5)]
    )

    last_modified = models.DateTimeField(
        auto_created=True,
        auto_now=True
    )

    parent_comment = TreeForeignKey(
        'self',
        verbose_name=_(u'parent comment'),
        blank=True,
        null=True
    )

    tree = TreeManager()

    def __unicode__(self):
        return _(u'From %s [%s]') % (self.user, self.get_last_modified())

    class Meta:
        verbose_name = _(u'Comment')
        verbose_name_plural = _(u'Comments')

    class MPTTMeta:
        parent_attr = 'parent_comment'
        order_insertion_by = 'last_modified'

    def get_last_modified(self):
        return formatdate(time.mktime(self.last_modified.timetuple()), usegmt=True)


def update_post(sender, instance, **kwargs):
    instance.post.comments_count = instance.post.comment_set.all().count()
    instance.post.save()
    Comment.tree.rebuild()

post_save.connect(update_post, Comment)
post_delete.connect(update_post, Comment)
