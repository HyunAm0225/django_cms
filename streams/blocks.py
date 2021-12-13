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


class RichTextblock(blocks.RichTextBlock):
    """ㄱ
    Richtext with all the features
    """

    class Meta:
        template = "streams/richtext_block.html"
        icon = "doc-full"
        label = "Full RichText"


class SimpleRichTextblock(blocks.RichTextBlock):
    """ㄱ
    Richtext with all the features
    """

    def __init__(
        self, required=True, help_text=None, editor="default", features=None, **kwargs
    ):
        super().__init__(**kwargs)
        self.features = [
            "bold",
            "italic",
            "link",
        ]

    class Meta:
        template = "streams/simple_richtext_block.html"
        icon = "edit"
        label = "Full RichText"
