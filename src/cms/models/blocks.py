__copyright__ = "Copyright 2017 Birkbeck, University of London"
__author__ = "Birkbeck Centre for Technology and Publishing"
__license__ = "AGPL v3"
__maintainer__ = "Birkbeck Centre for Technology and Publishing"

import random

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q, Max
from django.template.loader import get_template
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from model_utils.managers import InheritanceManager

from utils import setting_handler
from utils.logic import get_current_request


class CMSBlock(models.Model):
    """ An abstract class for implementing CMS blocks """
    objects = InheritanceManager()
    TEMPLATE = None
    # A page is divided in 12 columns
    ALLOWED_COLUMNS = ((4, "1/4"), (6, "1/2"), (8, "2/3"), (12, "1"))

    columns = models.PositiveIntegerField(blank=True, null=True, choices=ALLOWED_COLUMNS)
    sequence = models.PositiveIntegerField()
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

    @property
    def next_sequence(self):
        last_sequence = self.__class__.objects.filter(
            article=self.article,
            cms_block=self.cms_block,
        ).aggregate(Max("sequence"))["sequence__max"]
        if last_sequence is None:
            return 1
        else:
            return last_sequence + 1


    def save(self, *args, **kwargs):
        if not self.sequence:
            self.sequence = self.next_sequence
        super().save(*args, **kwargs)



class HTMLBlock(CMSBlock):
    TEMPLATE = 'cms/blocks/html_block.html'
    content = models.TextField(null=True, blank=True)

    @property
    def context(self):
        return {"content": self.content}

    class Meta:
        verbose_name="HTML Block"
        verbose_name_plural="HTML Blocks"


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
            'about_content':  setting_handler.get_setting(
                'general', 'journal_description', self.page.journal
            ).value,
        }

    class Meta:
        verbose_name="About Block"
        verbose_name_plural="About Blocks"


class NewsBlock(CMSBlock):
    TEMPLATE = 'cms/blocks/news_block.html'
    total_articles = models.PositiveIntegerField(
            default=1,
            help_text="Maximum number of news articles to render",
    )

    @property
    def context(self):
        from comms import models as comms_models
        if self.page.journal:
            content_type = ContentType.objects.get_for_model(self.page.journal)
        else:
            content_type = ContentType.objects.get_for_model(self.page.press)

        news_items = comms_models.NewsItem.objects.filter(
            (Q(content_type=content_type) & Q(object_id=self.page.site.pk)) &
            (Q(start_display__lte=timezone.now()) | Q(start_display=None)) &
            (Q(end_display__gte=timezone.now()) | Q(end_display=None))
        ).order_by('-posted')[:self.total_articles]

        return {"news_items":news_items}

    class Meta:
        verbose_name="News Block"
        verbose_name_plural="News Blocks"


class FeaturedJournalsBlock(CMSBlock):
    TEMPLATE = 'cms/blocks/featured_journals_block.html'
    use_random_journals = models.BooleanField(default=False)
    featured_journals = models.ManyToManyField('journal.Journal',
        null=True,
        blank=True,
    )

    @property
    def random_journals(self):
        if self.page.press:
            journals = set(self.page.press.journals())
        elif self.page.journal:
            journals = set(self.page.journal.press.journals())

        sample_size = min(6, len(journals))
        return random.sample(journals, sample_size)

    @property
    def context(self):
        if self.use_random_journals:
            journals = self.random_journals
        else:
            journals = self.featured_journals.all()

        return {"featured_journals": journals}

    class Meta:
        verbose_name="Featured Journals Block"
        verbose_name_plural="Featured Journals Blocks"


class FeaturedArticlesBlock(CMSBlock):
    TEMPLATE = 'cms/blocks/featured_articles_block.html'
    featured_articles= models.ManyToManyField('submission.Article',
        through="cms.CMSFeaturedArticle",
        null=True,
        blank=True,
    )


    @property
    def context(self):
        return {
            "featured_articles": self.featured_articles.all(
            ).order_by("cmsfeaturedarticle__sequence")
        }


def get_user_from_request():
    request = get_current_request()
    if request and request.user and request.user.is_authenticated:
        return request.user
    return None


class CMSFeaturedArticle(models.Model):
    article = models.ForeignKey("submission.Article")
    cms_block = models.ForeignKey("cms.FeaturedArticlesBlock")
    sequence = models.PositiveIntegerField(blank=True, null=True)
    added = models.DateTimeField(default=timezone.now)
    added_by = models.ForeignKey('core.Account',
            default=get_user_from_request,
            null=True, blank=True,
    )


    class Meta:
        unique_together = ("article", "cms_block")

    @property
    def next_sequence(self):
        last_sequence = self.__class__.objects.filter(
            article=self.article,
            cms_block=self.cms_block,
        ).aggregate(Max("sequence"))["sequence__max"]
        if last_sequence is None:
            return 1
        else:
            return last_sequence + 1


    def save(self, *args, **kwargs):
        if not self.sequence:
            self.sequence = self.next_sequence
        super().save(*args, **kwargs)

