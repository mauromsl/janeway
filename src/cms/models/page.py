from django.db import models

from utils import model_utils


class CMSPage(model_utils.SiteRelationMixin, models.Model):
    title = models.CharField(max_length=300,
        help_text="Page name displayed at the top of the page",
    )
    builtin = models.BooleanField(default=False)

    class Meta:
        unique_together = ('journal', 'press', 'title')

    @property
    def end_row_indexes(self):
        """ Set of indexes at which a row of blocks should be terminated"""
        total_blocks = self.blocks.count()
        indexes = set()
        columns = 0
        for idx, block in enumerate(self.blocks.all().order_by("sequence")):
            columns += block.columns
            if columns == 12:
                indexes.add(idx)
                columns = 0
            elif columns > 12:
                #row overflow
                indexes.add(idx - 1)
                columns = block.columns

        # Handle last block not filling 12 columns
        if total_blocks > 0:
            indexes.add(idx)

        return indexes


class CustomPage(CMSPage):

    def get_queryset(self):
        return super(CustomPage, self).get_queryset().filter(builtin=False)

    class Meta:
        proxy = True


