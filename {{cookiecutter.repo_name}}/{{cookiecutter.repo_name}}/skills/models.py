from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
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

    def people(self):
        people = [
            n.person_page for n in self.skills_person_relationship.all()
        ]
        return people
    # We get this relationship from the people app using the related
    # name 'skills_person_relationship' that connects to the parent page
    # 'person_page'


class SkillsIndexPage(Page):
    """
    This is a page to list all the skills on the site
    """
    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Skills listing image'
    )

    introduction = models.TextField(
        help_text='Text to describe the index page',
        blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
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
