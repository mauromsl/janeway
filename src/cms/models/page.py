from django.db import models

from utils import model_utils


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


