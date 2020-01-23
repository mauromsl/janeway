from django.db import models


class SiteRelationMixin(models.Model):
    """
    Mixin for models whose objects are related to either a journal or a press
    """
    journal = models.ForeignKey('journal.Journal', blank=True, null=True)
    press = models.ForeignKey('press.Press', blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def site(self):
        return self.journal or self.press

    def save(self, *args, **kwargs):
        if not bool(self.journal) ^ bool(self.press):
            raise ValidationError(
                    " One and only one of press or journal must be set")
        return super().save(*args, **kwargs)
