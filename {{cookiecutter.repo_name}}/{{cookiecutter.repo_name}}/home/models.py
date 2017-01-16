from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailadmin.edit_handlers import (
        FieldPanel,
        MultiFieldPanel, StreamFieldPanel,
        PageChooserPanel
        )


class HomePage(Page):
    """
    This HomePage model defines the top page of the website
    """
    organisation_name = models.CharField("Who you are", max_length=254)

    strapline = models.CharField("Organisation strap line", max_length=254)

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='The image to introduce the site'
    )

    featured_page_1_text = models.CharField(max_length=35, blank=True)
    featured_page_1 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Choose an awesome page to feature.',
        verbose_name='First featured page'
    )

    featured_page_2_text = models.CharField(max_length=35, blank=True)
    featured_page_2 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Choose another awesome page.',
        verbose_name='Second featured page'
    )

    featured_page_3_text = models.CharField(max_length=35, blank=True)
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
            ImageChooserPanel('hero_image'),
            FieldPanel('strapline'),
            MultiFieldPanel([
                FieldPanel('featured_page_1_text'),
                PageChooserPanel('featured_page_1'),
            ], heading="Feature page 1"),
            MultiFieldPanel([
                FieldPanel('featured_page_2_text'),
                PageChooserPanel('featured_page_2'),
            ], heading="Feature page 2"),
            MultiFieldPanel([
                FieldPanel('featured_page_3_text'),
                PageChooserPanel('featured_page_3'),
            ], heading="Feature page 3"),
            FieldPanel('copyright_notice'),
        ]

    # Only let the root page be a parent
    parent_page_types = ['wagtailcore.Page']
