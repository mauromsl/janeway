__copyright__ = "Copyright 2017 Birkbeck, University of London"
__author__ = "Martin Paul Eve & Andy Byers"
__license__ = "AGPL v3"
__maintainer__ = "Birkbeck Centre for Technology and Publishing"

from django.contrib import admin
from cms import models

admin_list = [
    (models.NavigationItem,),
    (models.Page,),
    (models.HTMLBlock,),
    (models.AboutBlock,),
    (models.NewsBlock,),
    (models.FeaturedJournalsBlock,),
    (models.CMSPage,), #TODO: Add Fixture and remove this before pushing!!
    (models.CustomPage,),
]

[admin.site.register(*t) for t in admin_list]
