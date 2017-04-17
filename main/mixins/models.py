# -*- coding: utf-8 -*-
from email.utils import formatdate

import time
from django.db import models
from django.utils.translation import ugettext_lazy as _
from autoslug import AutoSlugField


class SitePageModel(models.Model):
    """
        Объект, у которого может быть своя персональная страница.
    """

    title = models.CharField(
        verbose_name=_(u'title'),
        max_length=1000
    )

    content = models.TextField(
        verbose_name=_(u'content'),
        blank=True,
    )

    order = models.SmallIntegerField(
        verbose_name=_(u'display order'),
        default=0,
    )

    display = models.BooleanField(
        verbose_name=_(u'display?'),
        default=False
    )

    slug = AutoSlugField(
        verbose_name=_(u'slug'),
        max_length=1000,
        populate_from='title',
        unique_with='title',
        always_update=False,
        editable=True
    )

    last_modified = models.DateTimeField(
        auto_created=True,
        auto_now=True
    )

    class Meta:
        abstract = True

    @models.permalink
    def get_absolute_url(self):
        return '/%s/' % self.slug

    def __unicode__(self):
        return u'%s' % self.title

    def get_title(self):
        return u'%s' % self.title

    def get_breadcrumbs(self):
        return (
            {
                'title': self.title,
                'url': self.get_absolute_url()
            },
        )

    @classmethod
    def get_published(cls):
        return cls.objects.filter(display=True)

    def get_last_modified(self):
        return formatdate(time.mktime(self.last_modified.timetuple()), usegmt=True)
