__copyright__ = "Copyright 2017 Birkbeck, University of London"
__author__ = "Martin Paul Eve & Andy Byers"
__license__ = "AGPL v3"
__maintainer__ = "Birkbeck Centre for Technology and Publishing"


from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.template.loader import get_template

from utils import model_utils
from utils.logic import build_url_for_request

from model_utils.managers import InheritanceManager


class CMSPage(model_utils.SiteRelationMixin, models.Model):
    title = models.CharField(max_length=300,
        help_text="Page name displayed at the top of the page",
    )
    builtin = models.BooleanField(default=False)

    class Meta:
        unique_together = ('journal', 'press', 'title')


class CustomPage(CMSPage):

    def get_queryset(self):
        return super(CustomPage, self).get_queryset().filter(builtin=False)

    class Meta:
        proxy = True


class CMSBlock(models.Model):
    """ An abstract class for implementing CMS blocks """
    objects = InheritanceManager()
    TEMPLATE = None
    # A page is divided in 12 columns
    ALLOWED_COLUMNS = ((4, "1/4"), (6, "1/2"), (8, "2/3"), (12, "1"))

    columns = models.PositiveIntegerField(blank=True, null=True, choices=ALLOWED_COLUMNS)
    page = models.ForeignKey("cms.CMSPage",
        on_delete=models.CASCADE,
        related_name="blocks",
    )

    def render(self, loader=None):
        if loader is None:
            template = get_template(self.TEMPLATE)
        else:
            template = loader.get_template(self.TEMPLATE)
        return template.render(context=self.context)

    @property
    def context(self):
        """ The context required to render this block"""
        return {}


class HTMLBlock(CMSBlock):
    TEMPLATE = 'cms/blocks/html_block.html'
    content = models.TextField(null=True, blank=True)

    @property
    def context(self):
        return {"content": self.content}


class AboutBlock(CMSBlock):
    TEMPLATE = 'cms/blocks/about_block.html'
    title = models.CharField(
        max_length=300,
        help_text="Title to be displayed above the journal description"
    )

    @property
    def context(self):
        return {
            'title': self.title,
        }


class Page(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='page_content', null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    object = GenericForeignKey('content_type', 'object_id')

    name = models.CharField(max_length=300, help_text="Page name displayed in the URL bar eg. about or contact")
    display_name = models.CharField(max_length=100, help_text='Name of the page, max 100 chars, displayed '
                                                              'in the nav and on the header of the page eg. '
                                                              'About or Contact')
    content = models.TextField(null=True, blank=True)
    is_markdown = models.BooleanField(default=True)
    edited = models.DateTimeField(auto_now=timezone.now)

    def __str__(self):
        return u'{0} - {1}'.format(self.content_type, self.display_name)


class NavigationItem(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='nav_content', null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    object = GenericForeignKey('content_type', 'object_id')

    link_name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    is_external = models.BooleanField(default=False)
    sequence = models.IntegerField(default=99)
    page = models.ForeignKey(Page, blank=True, null=True)
    has_sub_nav = models.BooleanField(default=False, verbose_name="Has Sub Navigation")
    top_level_nav = models.ForeignKey("self", blank=True, null=True, verbose_name="Top Level Nav Item")

    def __str__(self):
        return self.link_name

    def sub_nav_items(self):
        return NavigationItem.objects.filter(top_level_nav=self)

    @property
    def build_url_for_request(self):
        if self.is_external:
            return self.link
        else:
            return build_url_for_request(path=self.link)

    @property
    def url(self):
        #alias for backwards compatibility with templates
        return self.build_url_for_request

    @classmethod
    def toggle_collection_nav(cls, issue_type):
        """Toggles a nav item for the given issue_type
        :param `journal.models.IssueType` issue_type: The issue type to toggle
        """

        defaults = {
            "link_name": issue_type.plural_name,
            "link": "/collections/%s" % (issue_type.code),
        }
        content_type = ContentType.objects.get_for_model(issue_type.journal)

        nav, created = cls.objects.get_or_create(
            content_type=content_type,
            object_id=issue_type.pk,
            defaults=defaults,
        )

        if not created:
            nav.delete()

    @classmethod
    def get_content_nav_for_journal(cls, journal):
        for issue_type in journal.issuetype_set.filter(
            ~Q(code="issue") # Issues have their own navigation
        ):
            try:
                content_type = ContentType.objects.get_for_model(
                    issue_type.journal)
                yield issue_type, cls.objects.get(
                    content_type=content_type,
                    object_id=issue_type.pk,
                )
            except cls.DoesNotExist:
                yield issue_type, None
