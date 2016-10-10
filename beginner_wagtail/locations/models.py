from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import (
        FieldPanel, InlinePanel, StreamFieldPanel)
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from beginner_wagtail.blocks import GlobalStreamBlock


class LocationPage(Page):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Location image'
    )

    body = StreamField(
        GlobalStreamBlock(), verbose_name="Person's biography", blank=True
        )
    # We've defined the StreamBlock() within blocks.py that we've imported on
    # line 12. Defining it in a different file

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
    ]

    parent_page_types = [
        'LocationIndexPage'
    ]

    # Defining what content type can sit under the parent
    subpage_types = [
    ]


class LocationIndexPage(Page):
    """
    This is a page to list all the locations on the site
    """
    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]

    introduction = models.TextField(
        help_text='Text to describe the index page',
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction')
    ]

    parent_page_types = [
        'home.HomePage'
    ]

    # Defining what content type can sit under the parent
    subpage_types = [
        'LocationPage'
    ]

# Strictly speaking this isn't necessary since it's just doing the default
# behaviour of Wagtail e.g. gets all person pages that are my descendent, show
# them if they're published ('live') and order by their first published date
# Docs http://docs.wagtail.io/en/v1.6.3/topics/pages.html#template-context
    def get_context(self, request):
        context = super(LocationIndexPage, self).get_context(request)
        context['skills'] = LocationPage.objects.descendant_of(
            self).live().order_by(
            '-first_published_at')
        return context
