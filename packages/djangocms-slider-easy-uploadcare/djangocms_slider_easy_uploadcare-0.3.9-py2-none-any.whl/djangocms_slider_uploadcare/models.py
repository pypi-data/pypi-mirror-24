from cms.models import CMSPlugin, Page
from cms.utils.compat.dj import python_2_unicode_compatible
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from pyuploadcare.dj.models import ImageField

try:
    from cms.models import get_plugin_media_path
except ImportError:
    def get_plugin_media_path(instance, filename):
        """
        See cms.models.pluginmodel.get_plugin_media_path on django CMS 3.0.4+
        for information
        """
        return instance.get_media_path(filename)


@python_2_unicode_compatible
class UploadcareSlide(CMSPlugin):
    """
    A Slide plugin that contains an image and some text.
    """

    image = ImageField(manual_crop="", )
    url = models.CharField(
        _("link"), max_length=255, blank=True, null=True,
        help_text=_("If present, clicking on image will take user to link. The link must begin with http:// or https://"))

    page_link = models.ForeignKey(
        Page, verbose_name=_("page"), null=True,
        limit_choices_to={'publisher_is_draft': True}, blank=True,
        help_text=_("If present, clicking on image will take user to "
                    "specified page."))

    caption = models.TextField(
        _("caption"), max_length=255, blank=True, null=True,
        help_text=_("Specifies text that occurs on the slide."))

    def __str__(self):
        if self.caption:
            return self.caption[:40]
        else:
            return self.image.info().get('original_filename')

    def clean(self):
        if self.url and self.page_link:
            raise ValidationError(
                _("You can enter a Link or a Page, but not both."))


@python_2_unicode_compatible
class UploadcareSlider(CMSPlugin):
    """
    Plugin that can contain Slides.
    """

    def __str__(self):
        return _(u"%s Images") % self.cmsplugin_set.all().count()
