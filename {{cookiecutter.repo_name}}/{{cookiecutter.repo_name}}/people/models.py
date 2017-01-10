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
from thefellowship.blocks import GlobalStreamBlock


@register_snippet
class PersonStatus(ClusterableModel):
    """
    This snippet allows an editor to define what possible employment statuses
    a staff member may have.
    """

    search_fields = Page.search_fields + [
        index.SearchField('title'),
    ]

    title = models.CharField("Status", max_length=254)

    panels = [
        FieldPanel('title'),
    ]

    def __str__(self):
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
    'related_name'.
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
    `locations` app, and the PersonPage below
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
    app and the PersonPage below allowing us to add skills to a person
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
    # line 12. Defining it in a different file

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

    parent_page_types = [
        'PersonIndexPage'
    ]

    # Defining what content type can sit under the parent
    subpage_types = [
    ]

    api_fields = [
        'image',
        'body',
        'person_skills_relationship',
        'person_employment_relationship',
        'person_location_relationship',
    ]

    # We iterate within the model over the skills, status
    # and location so we don't have to on the template
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


class PersonIndexPage(Page):
    """
    This is a page to list all the people on the site
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
        'PersonPage'
    ]

# Strictly speaking this isn't necessary since it's just doing the default
# behaviour of Wagtail e.g. gets all person pages that are my descendent, show
# them if they're published ('live') and order by their first published date
# Docs http://docs.wagtail.io/en/v1.6.3/topics/pages.html#template-context
    def get_context(self, request):
        context = super(PersonIndexPage, self).get_context(request)
        context['people'] = PersonPage.objects.descendant_of(
            self).live().order_by(
            '-first_published_at')
        return context
