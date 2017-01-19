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
    # Setting an empty array means that no child page can be added to this page type

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

    def parent_url(self):
        parent_set = Page.objects.parent_of(
                self).all()
        # Get all objects for the parent page within a queryset using
        # Treebeard's `parent_of`

        parent_url_string = [n.url for n in parent_set]
        # Get the URL out of the queryset
        # If you try to access it directly you'll hit the error:
        # 'PageQuerySet' object has no attribute 'url'

        for object in parent_url_string:
            return object
        # The PageQuerySet behaves exactly as you'd expect it to
        # meaning that you could loop over the `parent_set` in the template
        # by doing:
        #   {% for object in parent_set %}
        #       {{ object.url }}
        #   {% endfor %}


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

# Below we return the context so that we can access `skills`
# within our templates. The `skills` context is doing exactly what Wagtail would
# do out of the box (e.g. display all live descendants of the index page and
# order them by their publication date)
# More info
# Docs http://docs.wagtail.io/en/v1.8/topics/pages.html#template-context
    def get_context(self, request):
        context = super(SkillsIndexPage, self).get_context(request)
        context['skills'] = SkillsPage.objects.descendant_of(
            self).live().order_by(
            '-first_published_at')
        return context
