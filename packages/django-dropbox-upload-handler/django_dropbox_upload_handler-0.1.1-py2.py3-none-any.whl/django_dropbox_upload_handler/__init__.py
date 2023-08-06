__version__ = '0.1.1'
from django.conf import settings
from django.core.checks import Error, register
@register()
def check_settings(app_configs, **kwargs):
    errors = []
    handler_settings = getattr(settings, "DROPBOX_UPLOAD_HANDLER", None)
    if handler_settings is None:
        errors.append(
            Error(
                "Missing 'DROPBOX_UPLOAD_HANDLER' dict in settings",
                hint="Add 'DROPBOX_UPLOAD_HANDLER' to your settings",
                obj=settings,
                id='django_dropbox_upload_handler.001'
            )
        )
    else:
        token = handler_settings.get('ACCESS_TOKEN', None)
        if token is None:
            errors.append(
                Error(
                    "Missing 'ACCESS_TOKEN' setting",
                    hint="Add 'ACCESS_TOKEN': 'token_value' in' 'DROPBOX_UPLOAD_HANDLER' within your settings",
                    obj=settings.DROPBOX_UPLOAD_HANDLER,
                    id="django_dropbox_upload_handler.002"
                )
            )
        elif token == '':
            errors.append(
                Error(
                    "'ACCESS_TOKEN' is empty",
                    hint="Add 'ACCESS_TOKEN': 'token_value'",
                    obj=settings.DROPBOX_UPLOAD_HANDLER,
                    id="django_dropbox_upload_handler.002"
                )
            )
    return errors
