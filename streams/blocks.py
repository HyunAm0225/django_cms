from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


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


class CardBlock(blocks.StructBlock):
    """
    cards with image and text and button(s).
    """

    title = blocks.CharBlock(required=True, help_text="add your title")

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", blocks.CharBlock(required=True, max_length=40)),
                ("text", blocks.TextBlock(required=True, max_length=200)),
                ("button_page", blocks.PageChooserBlock(required=False)),
                (
                    "button_url",
                    blocks.URLBlock(
                        required=False,
                        help_text="If the button page above is selected, that will be used first.",
                    ),
                ),
            ]
        )
    )

    class Meta:
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "Staff Cards"


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


class CTABlock(blocks.StructBlock):
    """
    A simple call to action section
    """

    title = blocks.CharBlock(require=True, max_length=60)
    text = blocks.RichTextBlock(required=True, features=["bold", "italic"])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(
        required=True,
        default="Learn More",
    )

    class Meta:  # noqa
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to Action"


class LinkStructValue(blocks.StructValue):
    """Additional logic for our urls."""

    def url(self):
        button_page = self.get("button_page")
        button_url = self.get("button_url")

        if button_page:
            return button_page.url
        elif button_url:
            return button_url
        else:
            return None

    # def latest_posts(self):
    #     return BlogPage.objects.live()[:3]


class ButtonBlock(blocks.StructBlock):
    """An external or internal URL."""

    button_page = blocks.PageChooserBlock(
        required=False, help_text="If selected, this url will be used first"
    )
    button_url = blocks.URLBlock(
        required=False,
        help_text="If added, this url will be used secondarily to the button page",
    )

    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)
    #     context["latest_posts"] = BlogPage.objects.live().public()[:3]
    #     return context

    class Meta:  # noqa
        template = "streams/button_block.html"
        icon = "placeholder"
        label = "Single Button"
        value_class = LinkStructValue
