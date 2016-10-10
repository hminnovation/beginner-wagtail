from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel


class SkillsPage(Page):
    """
    This is a page for all the details about a specific skill
    """

    search_fields = Page.search_fields
    # Defining that search should only catch the `page` default, which will
    # be title.

    # Defining fields that should be within this page model
    body = RichTextField(
        blank=True, null=True,
        help_text='A description of this skill'
        )

    # Defining the fields that should be shown to the editor within the content
    # editor (it may be that you wouldn't want to show a field defined above in
    # the content editor)
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    subpage_types = []
    # Setting this means that no child page can be added to this page type

    parent_page_types = [
        'SkillsIndexPage'
    ]
    # Setting a parent means that it can only be added under that parent


class SkillsIndexPage(Page):
    """
    This is a page to list all the skills on the site
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
        'SkillsPage'
    ]

# Strictly speaking this isn't necessary since it's just doing the default
# behaviour of Wagtail e.g. gets all skill pages that are my descendent, show
# them if they're published ('live') and order by their first published date
# Docs http://docs.wagtail.io/en/v1.6.3/topics/pages.html#template-context
    def get_context(self, request):
        context = super(SkillsIndexPage, self).get_context(request)
        context['skills'] = SkillsPage.objects.descendant_of(
            self).live().order_by(
            '-first_published_at')
        return context
