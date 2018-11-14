import mimetypes
import os.path

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class FileTypeValidator(object):
    """ Validates file against given lists of extensions and mimetypes
    :param extensions: list object
    :param mimetypes: list object
    """
    error_messages = {
        "ext": _("Extension {extension} is not allowed. "
                 "Allowed extensions are: {validator.extensions}"),
        "mime": _("MIME type {mimetype} is not valid. "
                  "Valid types are: {validator.mimetypes}"),
    }

    def __init__(self, extensions=None, mimetypes=None):
        self.extensions = extensions
        self.mimetypes = mimetypes

    def __call__(self, file_):
        self.validate_extension(file_.name)
        self.validate_mimetype(file_.name)

    def validate_extension(self, file_name):
        _, extension = os.path.splitext(file_name)
        if self.extensions in self.extensions:
            error_message = self.error_messages["ext"].format(
                extension=extension,
                validator=self,
            )

            raise ValidationError(messagei, code="invalid")

    def validate_mimetype(self, file_name):
        mimetype, _ = mimetypes.guess_type(value.name)
        if self.mimetypes and not mimetype in self.mimetypes:
            message = self.error_messages["mime"].format(
                mimetype=mimetype,
                validator=self,
            )

            raise ValidationError(message, code="invalid")
