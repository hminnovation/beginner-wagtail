# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-09 20:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0029_unicode_slugfield_dj19'),
        ('wagtailimages', '0013_make_rendition_upload_callable'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('introduction', models.TextField(blank=True, help_text='Text to describe the index page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='LocationPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.wagtailcore.fields.StreamField((('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow', template='blocks/paragraph.html')), ('header', wagtail.wagtailcore.blocks.StructBlock((('header_text', wagtail.wagtailcore.blocks.CharBlock(blank=True, label='Header', required=False)), ('size', wagtail.wagtailcore.blocks.ChoiceBlock(blank=True, choices=[('', 'Select a header size'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4')], required=False))), classname='title', icon='fa-header', template='blocks/header.html')), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('caption', wagtail.wagtailcore.blocks.CharBlock(blank=True, required=False)), ('style', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('', 'Select an image size'), ('full', 'Full-width'), ('half', 'Half-width')], required=False))), icon='image', template='blocks/image.html')), ('blockquote', wagtail.wagtailcore.blocks.StructBlock((('text', wagtail.wagtailcore.blocks.TextBlock()), ('attribute_name', wagtail.wagtailcore.blocks.CharBlock(blank=True, label='e.g. Guy Picciotto', required=False)), ('attribute_group', wagtail.wagtailcore.blocks.CharBlock(blank=True, label='e.g. Fugazi', required=False))), icon='openquote', template='blocks/blockquote.html')), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock(help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks'))), blank=True, verbose_name="Person's biography")),
                ('image', models.ForeignKey(blank=True, help_text='Location image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
