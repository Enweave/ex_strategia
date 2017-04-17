from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from main.views import post_detail, post_list, post_comment, load_comments

admin.site.site_header = u'Commentarium'
admin.site.site_title = u'Commentarium'
admin.site.index_title = u'Commentarium'

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^admin/', admin.site.urls),
    url(
        r'^posts/$',
        post_list,
        name='post-list'
    ),
    url(
        r'^post-comment/$',
        post_comment,
        name='post-comment'
    ),
    url(
        r'^load_comments/$',
        load_comments,
        name='load-comments'
    ),
    url(
        r'^posts/(?P<slug>([-\w\d]+){1,30})/$',
        post_detail,
        name='post-detail'
    ),
    # url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)