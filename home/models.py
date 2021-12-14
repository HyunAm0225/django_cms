from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
    PageChooserPanel,
)
from wagtail.core.models import Orderable, Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.contrib.routable_page.models import RoutablePage, RoutablePageMixin, route
from wagtail.images.edit_handlers import ImageChooserPanel

from streams import blocks


class homPageCarouseImages(Orderable):
    """
    between 1 and 5 images for the home page carousel.
    """

    page = ParentalKey("home.Homepage", related_name="carousel_images")
    carousel_images = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [ImageChooserPanel("carousel_images")]


class HomePage(RoutablePageMixin, Page):
    """Home page model."""

    template = "home/home_page.html"
    max_count = 1

    banner_title = models.CharField(max_length=100, blank=False, null=True)
    banner_subtitle = RichTextField(features=["bold", "italic"], null=True, blank=True)
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    banner_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content = StreamField(
        [
            ("cta", blocks.CTABlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("banner_title"),
                FieldPanel("banner_subtitle"),
                ImageChooserPanel("banner_image"),
                PageChooserPanel("banner_cta"),
            ],
            heading="banner options",
        ),
        StreamFieldPanel("content"),
        MultiFieldPanel(
            [
                InlinePanel("carousel_images", max_num=5, min_num=1, label=""),
            ],
            heading="Carousel Images",
        ),
    ]

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"

    @route(r"^subscribe/$")
    def the_subscribe_page(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context["a_special_text"] = "Hello_world123123123"
        return render(request, "home/subscribe.html", context)
