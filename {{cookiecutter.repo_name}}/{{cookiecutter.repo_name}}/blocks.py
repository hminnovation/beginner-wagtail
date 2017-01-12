from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailcore.blocks import (
    StructBlock,
    TextBlock,
    StreamBlock,
    RichTextBlock,
    CharBlock,
    ChoiceBlock
)
# Note, you could import _all_ the blocks by using `from wagtail.wagtailcore
# import blocks`. But it's a bad idea to import everything.
# Docs: http://docs.wagtail.io/en/latest/topics/streamfield.html


class GlobalStreamBlock(StreamBlock):
    paragraph = RichTextBlock(
        icon="pilcrow",
        template="blocks/paragraph.html"
    )
    header = StructBlock([
        ('header_text', CharBlock(
            blank=True, required=False, label='Header')),
        ('size', ChoiceBlock(choices=[
            ('', 'Select a header size'),
            ('h2', 'H2'),
            ('h3', 'H3'),
            ('h4', 'H4')
        ], blank=True, required=False))
        ],
        classname="title",
        icon="title",
        template="blocks/header.html")
    image = StructBlock([
        ('image', ImageChooserBlock()),
        ('caption', CharBlock(blank=True, required=False)),
        ('style', ChoiceBlock(choices=[
            ('', 'Select an image size'),
            ('full', 'Full-width'),
            ('half', 'Half-width')
        ], required=False))
    ], icon="image", template="blocks/image.html")
    blockquote = StructBlock([
        ('text', TextBlock()),
        ('attribute_name', CharBlock(
            blank=True, required=False, label='e.g. Guy Picciotto')),
        ('attribute_group', CharBlock(
            blank=True, required=False, label='e.g. Fugazi')),
    ], icon="openquote", template="blocks/blockquote.html")
    embed = EmbedBlock(
        help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks')
