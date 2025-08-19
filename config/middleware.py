from django.conf import settings
from django.utils import translation

class QueryStringLocaleMiddleware:
    """
    Activa el idioma a partir de ?lang=es|en.
    Debe ir DESPUÉS de django.middleware.locale.LocaleMiddleware (ya lo agregamos en dev.py).
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.valid_languages = {code for code, _ in getattr(settings, "LANGUAGES", [("es", "Español")])}

    def __call__(self, request):
        lang = request.GET.get("lang")
        if lang and lang in self.valid_languages:
            translation.activate(lang)
            request.LANGUAGE_CODE = lang

        response = self.get_response(request)

        if lang and lang in self.valid_languages:
            translation.deactivate()

        return response
