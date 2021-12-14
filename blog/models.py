from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey
from streams import blocks
from wagtail.core.models import Orderable, Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.contrib.routable_page.models import RoutablePage, RoutablePageMixin, route
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    StreamFieldPanel,
    InlinePanel,
)
from wagtail.snippets.models import register_snippet
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.search import index


class BlogAuthorsOrderable(Orderable):
    page = ParentalKey("blog.BlogDetailpage", related_name="blog_authors")
    author = models.ForeignKey(
        "blog.blogAuthor",
        on_delete=models.CASCADE,
    )
    panels = [
        SnippetChooserPanel("author"),
    ]


class BlogAuthor(models.Model):
    """blog author for snippets."""

    name = models.CharField(
        max_length=100,
    )
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                ImageChooserPanel("image"),
            ],
            heading="Name and Image",
        ),
        MultiFieldPanel(
            [
                FieldPanel("website"),
            ],
            heading="Links",
        ),
    ]

    def __str__(self):
        """string repr of this class"""
        return self.name

    class Meta:  # noqa
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"


register_snippet(BlogAuthor)


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
        context["authors"] = BlogAuthor.objects.all()
        return context

    @route(r"^latest/$", name="latest_post")
    def latest_blog_posts(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        # context["posts"] = context["posts"][:1]
        context["latest_posts"] = BlogPage.objects.live().public()[:1]
        return render(request, "blog/latest_posts.html", context)

    def get_sitemap_urls(self, request):
        sitemap = super().get_sitemap_urls(request)
        sitemap.append(
            {
                "location": self.full_url + self.reverse_subpage("latest_post"),
                "lastmod": (self.last_published_at or self.latest_revision_created_at),
                "priority": 0.9,
            }
        )
        return sitemap


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
            ("full_richtext", blocks.RichTextblock()),
            ("title_and_text", blocks.TitleAndTextBlock()),
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
        MultiFieldPanel(
            [
                InlinePanel("blog_authors", label="Author", min_num=1, max_num=4),
            ],
            heading="Author(s)",
        ),
        StreamFieldPanel("content"),
    ]
