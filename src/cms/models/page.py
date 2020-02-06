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

    @property
    def structure(self):
        return self.get_structure()

    def get_structure(self, select_subclasses=False):
        """ GenExp that yields the blocks of this page in column-based rows
        e.g:
            >>> [12, 6, 12, 6, 6, 4, 4, 4, 12, 7]
            [[12], [6],[12], [6, 6], [4,4,4],[12], [7]]
        """
        blocks = self.blocks.all().order_by("sequence")
        if select_subclasses:
            blocks = self.blocks.select_subclasses().order_by("sequence")
        columns = 0
        row = []

        for block in blocks:
            filled, columns = self.check_row(columns, row, block)
            if filled:
                yield row
                row = [block]
            else:
                row.append(block)
        yield row


    @staticmethod
    def check_row(columns, row, block):
        if columns >= 12 or columns + block.columns > 12:
            return True, block.columns
        return False, columns + block.columns



class CustomPage(CMSPage):

    def get_queryset(self):
        return super(CustomPage, self).get_queryset().filter(builtin=False)

    class Meta:
        proxy = True


