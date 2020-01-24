__copyright__ = "Copyright 2017 Birkbeck, University of London"
__author__ = "Birkbeck Centre for Technology and Publishing"
__license__ = "AGPL v3"
__maintainer__ = "Birkbeck Centre for Technology and Publishing"


from django.db import models
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _

from model_utils.managers import InheritanceManager

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


