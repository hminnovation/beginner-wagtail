from __future__ import unicode_literals

from django.db import models

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import (
        FieldPanel,
        InlinePanel,
        StreamFieldPanel,
        PageChooserPanel
        )
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from {{cookiecutter.repo_name}}.blocks import GlobalStreamBlock


@register_snippet
class PersonStatus(ClusterableModel):
    """
    This snippet allows an editor to define what possible employment statuses
    a staff member may have. Or whether they're a wizard...
    """

    search_fields = Page.search_fields + [
        index.SearchField('title'),
    ]

    title = models.CharField("Status", max_length=254)

    panels = [
        FieldPanel('title'),
    ]

    def __str__(self):
        # We have to return a string to populate the snippets screen. The
        # Snippets admin screen will only support a string
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = "Status"
        verbose_name_plural = "Statuses"


class PersonStatusRelationship(models.Model):
    """
    This defines the relationship between the `PersonEmploymentStatus` snippet
    above and the PersonPage below. It does so by defining a ForeignKey
    relationship between the two, which can be accessed by the respective
    'related_name'. The magic key is the 'related_name'
    Docs: http://www.tivix.com/blog/working-wagtail-i-want-my-m2ms/
    """
    person_page = ParentalKey(
        'PersonPage', related_name='person_status_relationship'
    )
    person_statuses = models.ForeignKey(
        'PersonStatus',
        related_name="status_person_relationship"
    )
    panels = [
        SnippetChooserPanel('person_statuses')
    ]


class PersonLocationRelationship(models.Model):
    """
    This defines the relationship between the `LocationPage`, within the
    `locations` app, and the PersonPage below. Again the magic key is
    the related_name. On the LocationPage model in the locations app you can
    see the reverse relationship of the related_name being used to populate
    people on the LocationPage
    """
    person_page = ParentalKey(
        'PersonPage', related_name='person_location_relationship'
    )
    location = models.ForeignKey(
        'locations.LocationPage',
        related_name="location_person_relationship"
    )
    panels = [
        PageChooserPanel('location')
    ]


class PersonSkillsRelationship(Orderable, models.Model):
    """
    This defines the relationship between the `SkillPage` within the `skills`
    app and the PersonPage below allowing us to add skills to a person. As above
    the magic key is the related_name
    """
    person_page = ParentalKey(
        'PersonPage', related_name='person_skills_relationship'
    )
    skills = models.ForeignKey(
        'skills.SkillsPage', related_name='skills_person_relationship'
    )
    panels = [
        PageChooserPanel('skills')
    ]


class PersonPage(Page):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Person image'
    )

    body = StreamField(
        GlobalStreamBlock(), verbose_name="Person's biography", blank=True
        )
    # We've defined the StreamBlock() within blocks.py that we've imported on
    # line 20. Defining it in a different file aids consistency across the site
    # but it can be defined on a per page basis if that's helpful for you

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
        InlinePanel(
            'person_skills_relationship',
            label='Skills',
            min_num=None
            ),
        InlinePanel(
            'person_status_relationship',
            label='Status',
            min_num=None,
            max_num=1
            ),
        InlinePanel(
            'person_location_relationship',
            label='Location',
            min_num=None,
            max_num=1
            ),
    ]

    # Defining the parent. This means the editor will only be able to add the
    # page under a PersonIndexPage and won't see that the PersonPage exists as
    # an option until that parent page has been added.
    parent_page_types = [
        'PersonIndexPage'
    ]

    # Defining what content type can sit under the parent
    # The empty array will mean no children can be added
    subpage_types = []

    # We iterate within the model over the skills, status
    # and location so they can be accessible to the template
    def skills(self):
        skills = [
            n.skills for n in self.person_skills_relationship.all()
        ]
        return skills

    def status(self):
        status = [
            n.person_statuses for n in self.person_status_relationship.all()
        ]
        return status

    def location(self):
        location = [
            n.location for n in self.person_location_relationship.all()
        ]
        return location

    # For ForeignKeys that we want to access via the API we need to explictly
    # access a specific field from the related content. I've added unnecessary
    # verbosity here because we could use the `skills(self)` method above to
    # give us the objects in a list within the for loop.
    # This isn't terribly useful since I'm only returning the title but hopefully
    # enough to be extendable/ understandable
    def skills_object(obj):
        skills_set = obj.person_skills_relationship.all()
        skills = [
            n.skills for n in skills_set
        ]
        for skill in skills:
            return skill.title

    api_fields = [
        'image',
        'body',
        'skills_object'
    ]


class PersonIndexPage(Page):
    """
    This is a page to list all the people on the site
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
        help_text='People listing image'
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
        'PersonPage'
    ]

# We're using get context to organise alphabetically
# Docs http://docs.wagtail.io/en/v1.6.3/topics/pages.html#template-context
    def get_context(self, request):
        context = super(PersonIndexPage, self).get_context(request)
        context['people'] = PersonPage.objects.descendant_of(
            self).live().order_by(
            'title')
        return context
