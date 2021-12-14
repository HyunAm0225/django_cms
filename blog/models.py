from django.db import models
from django.shortcuts import render

from streams import blocks
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.contrib.routable_page.models import RoutablePage, RoutablePageMixin, route
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index


class BlogIndexPage(RoutablePageMixin, Page):
    intro = RichTextField(blank=True)

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        help_text="Overwrites the default title",
    )
    content_panels = Page.content_panels + [
        FieldPanel("intro", classname="full"),
        FieldPanel("custom_title"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = BlogPage.objects.live().public()
        context["regular_context_var"] = "Hello world 123123123"
        return context

    @route(r"^latest/$", name="latesst_post")
    def latest_blog_posts(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        # context["posts"] = context["posts"][:1]
        context["latest_posts"] = BlogPage.objects.live().public()[:1]
        return render(request, "blog/latest_posts.html", context)


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("body", classname="full"),
    ]


class BlogDetailPage(Page):
    """blog detail page"""

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        help_text="Overwrites the default title",
    )
    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichTextblock()),
            ("simple_richtext", blocks.SimpleRichTextblock()),
            ("cards", blocks.CardBlock()),
            ("cta", blocks.CTABlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        ImageChooserPanel("blog_image"),
        StreamFieldPanel("content"),
    ]
