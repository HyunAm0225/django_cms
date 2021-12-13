from wagtail.core import blocks


class TitleAndTextBlock(blocks.StructBlock):
    """
    Title and text and nothing else
    """

    title = blocks.CharBlock(required=True, help_text="Add yourt title")
    text = blocks.TextBlock(required=True, help_text="Add yourt text")

    class Meta:
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"