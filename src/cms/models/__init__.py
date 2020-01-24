__copyright__ = "Copyright 2017 Birkbeck, University of London"
__author__ = "Birkbeck Centre for Technology and Publishing"
__license__ = "AGPL v3"
__maintainer__ = "Birkbeck Centre for Technology and Publishing"

from cms.models.blocks import (
    CMSBlock,
    HTMLBlock,
    AboutBlock,
)

from cms.models.page import (
    CMSPage,
    CustomPage,
)

from cms.models.old_models import (
    Page,
    NavigationItem,

)

__all__ = {
    "CMSBlock",
    "HTMLBlock",
    "AboutBlock",

    "CMSPage",
    "CustomPage",

    "Page",
    "NavigationItem",
}
