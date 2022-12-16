__copyright__ = "Copyright 2017 Birkbeck, University of London"
__author__ = "Martin Paul Eve, Andy Byers & Mauro Sanchez"
__license__ = "AGPL v3"
__maintainer__ = "Birkbeck Centre for Technology and Publishing"

from django.contrib import admin
from utils import admin_utils
from discussion import models
from core.templatetags.truncate import truncatesmart


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subject', 'owner', 'started', 'object_title',
                    'journal')
    list_filter = ('article__journal', 'subject', 'started', 'last_updated')
    search_fields = ('pk', 'article__title', 'preprint__title',
                     'subject', 'owner__first_name', 'owner__last_name',
                     'owner__email', 'post__body')
    raw_id_fields = ('owner', 'article', 'preprint')
    date_hierarchy = ('last_updated')

    inlines = [
        admin_utils.PostInline
    ]

    def journal(self, obj):
        return obj.article.journal if obj else ''


class PostAdmin(admin.ModelAdmin):
    list_display = ('post', 'thread', 'owner', 'posted', 'journal')
    list_filter = ('thread__article__journal', 'posted')
    search_fields = ('pk', 'body', 'thread__subject', 'owner__first_name',
                     'owner__last_name', 'owner__email',)
    raw_id_fields = ('thread', 'owner',)
    filter_horizontal = ('read_by',)
    save_as = True
    date_hierarchy = ('posted')

    def journal(self, obj):
        return obj.thread.article.journal if obj else ''

    def post(self, obj):
        return truncatesmart(obj.body) if obj else ''


admin_list = [
    (models.Thread, ThreadAdmin),
    (models.Post, PostAdmin),
]

[admin.site.register(*t) for t in admin_list]
