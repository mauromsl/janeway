from django.test import TestCase
from cms.models import CMSBlock, CMSPage


class BlockTests(TestCase):

    def test_even_end_row_indexes(self):
        press, c = Press.objects.get_or_create(domain="blocks")
        page = CMSPage.objects.create(title="sometitle", press=press)
        full_width_block = CMSBlock.objects.create(columns=12, sequence=1, page=page)
        half_width_block_1 = CMSBlock.objects.create(columns=6, sequence=2, page=page)
        half_width_block_2 = CMSBlock.objects.create(columns=6, sequence=3, page=page)

        expected_indexes = {0,2}
        self.assertEqual(page.end_row_indexes, expected_indexes)

    def test_uneven_end_row_indexes(self):
        press, c = Press.objects.get_or_create(domain="blocks")
        page = CMSPage.objects.create(title="sometitle", press=press)
        full_width_block = CMSBlock.objects.create(columns=12, sequence=1, page=page)
        half_width_block_1 = CMSBlock.objects.create(columns=7, sequence=2, page=page)
        half_width_block_2 = CMSBlock.objects.create(columns=6, sequence=3, page=page)
        half_width_block_2 = CMSBlock.objects.create(columns=6, sequence=3, page=page)

        expected_indexes = {0,1,3}
        self.assertEqual(page.end_row_indexes, expected_indexes)

    def test_uneven_end_row_indexes_incomplete(self):
        press, c = Press.objects.get_or_create(domain="blocks")
        page = CMSPage.objects.create(title="sometitle", press=press)
        full_width_block = CMSBlock.objects.create(columns=12, sequence=1, page=page)
        half_width_block_1 = CMSBlock.objects.create(columns=9, sequence=2, page=page)
        half_width_block_2 = CMSBlock.objects.create(columns=6, sequence=3, page=page)
        half_width_block_2 = CMSBlock.objects.create(columns=3, sequence=3, page=page)


        expected_indexes = {0,1,3}
        self.assertEqual(page.end_row_indexes, expected_indexes)


    def test_end_row_indexes_no_blocks(self):
        press, c = Press.objects.get_or_create(domain="blocks")
        page = CMSPage.objects.create(title="sometitle", press=press)

        expected_indexes = set()
        self.assertEqual(page.end_row_indexes, expected_indexes)

    def test_page_structure(self):
        press, c = Press.objects.get_or_create(domain="blocks")
        page = CMSPage.objects.create(title="sometitle", press=press)
        A = CMSBlock.objects.create(columns=12, sequence=1, page=page)
        B = CMSBlock.objects.create(columns=6, sequence=2, page=page)
        C = CMSBlock.objects.create(columns=9, sequence=3, page=page)
        D = CMSBlock.objects.create(columns=4, sequence=4, page=page)
        E = CMSBlock.objects.create(columns=4, sequence=4, page=page)
        F = CMSBlock.objects.create(columns=4, sequence=4, page=page)
        G = CMSBlock.objects.create(columns=8, sequence=5, page=page)

        expected_result = [[A], [B], [C], [D, E, F], [G]]
        self.assertEqual(list(page.structure), expected_result)


