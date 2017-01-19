from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import (
        FieldPanel,
        MultiFieldPanel,
        PageChooserPanel
        )


class HomePage(Page):
    """
    The HomePage model references other pages to populate itself, grabbing the
    headline, introductory text and image from those pages. Note that the
    fields `organisation_name` and `copyright_notice` are used by the
    `navigation_tags.py` file to populate content in the header or footer across
    the entire site. Probably not ideal, but a shortcut to avoid creating another
    model to store that information somewhere.
    """

    organisation_name = models.CharField("Who you are", max_length=254)

    strapline = models.CharField("Organisation strap line", max_length=254)

    featured_page_1 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Choose an awesome page to feature.',
        verbose_name='First featured page'
    )

    featured_page_2 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Choose another awesome page.',
        verbose_name='Second featured page'
    )

    featured_page_3 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='You should probably add a third page too.',
        verbose_name='Third featured page'
    )

    copyright_notice = models.CharField(
        'Copyright notice to appear on footer pages',
        null=True,
        blank=True,
        max_length=526)

    content_panels = Page.content_panels + [
            FieldPanel('organisation_name'),
            FieldPanel('strapline'),
            MultiFieldPanel([
                PageChooserPanel('featured_page_1'),
            ], heading="Feature page 1"),
            MultiFieldPanel([
                PageChooserPanel('featured_page_2'),
            ], heading="Feature page 2"),
            MultiFieldPanel([
                PageChooserPanel('featured_page_3'),
            ], heading="Feature page 3"),
            FieldPanel('copyright_notice'),
        ]

    # Only let the root page be a parent
    # Docs docs.wagtail.io/en/v1.0b1/reference/page.html
    parent_page_types = ['wagtailcore.Page']
