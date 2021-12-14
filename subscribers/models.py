from django.db import models

# Create your models here.


class Subscribers(models.Model):
    """A subscriber model."""

    email = models.CharField(
        max_length=100, blank=False, null=False, help_text="email address"
    )
    full_name = models.CharField(
        max_length=100, blank=False, null=False, help_text="firstname and lastname"
    )

    def __str__(self):
        """
        Str repr of this object.
        """
        return self.full_name

    class Meta:  # noqa
        verbose_name = "Subscribers"
        verbose_name_plural = "Subscribers"
