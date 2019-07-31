from django.db.models.fields import TextField
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from core.models import DiscoverUniBasePage


class ContentLandingPage(DiscoverUniBasePage):
    options = StreamField([
        ('sections', blocks.PageChooserBlock())
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('options', classname="full")
    ]


class Section(DiscoverUniBasePage):
    subsections = StreamField([
        ('subsection', blocks.StructBlock([
            ('subsection_title', blocks.TextBlock()),
            ('subsection_content', blocks.RichTextBlock())
        ]))
    ])
    related_links_title = TextField(blank=True)
    related_links = StreamField([
        ('links', blocks.PageChooserBlock(required=False)),
    ], blank=True)
    lateral_link_title = TextField(blank=True)
    lateral_links = StreamField([
        ('links', blocks.PageChooserBlock(required=False)),
    ], blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('subsections'),
        FieldPanel('related_links_title'),
        StreamFieldPanel('related_links'),
        FieldPanel('lateral_link_title'),
        StreamFieldPanel('lateral_links')
    ]
