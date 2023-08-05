from django.conf import settings

PHRASE_ENABLED = getattr(settings, 'PHRASE_ENABLED', True)
PHRASE_PROJECT_ID = getattr(settings, 'PHRASE_PROJECT_ID', '')
PHRASE_PREFIX = getattr(settings, 'PHRASE_PREFIX', '{{__')
PHRASE_SUFFIX = getattr(settings, 'PHRASE_SUFFIX', '__}}')
PHRASE_JS_HOST = getattr(settings, 'PHRASE_JS_HOST', 'phraseapp.com')
PHRASE_JS_USE_SSL = getattr(settings, 'PHRASE_JS_USE_SSL', True)


def template_string_if_valid():
    try:  # does not throw an exception as of 1.11 yet
        value = settings.TEMPLATE_STRING_IF_INVALID
        if value:
            return value
    except:
        pass

    for templ in settings.TEMPLATES:
        if "OPTIONS" in templ:
            templ_options = templ["OPTIONS"]
            if 'string_if_invalid' in templ_options:
                return templ_options['string_if_invalid']

    return u''
