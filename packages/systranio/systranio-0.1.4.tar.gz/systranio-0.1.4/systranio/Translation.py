"""
Translation API

Usage :

```
import systranio

translation = systranio.Translation(API_KEY)
options = {'source': 'en' }
result = translation.text('traduction', 'fr', **options)
print(result)  # traduction
print(result.stats)  #  {"elapsed_time": 20, "nb_characters": 9, ...
```

"""

from .api import BaseAPI

TEXT_ENDPOINT = '/translation/text/translate'
API_VERSION_ENDPOINT = '/translation/apiVersion'
SUPPORTED_LANGUAGES_ENDPOINT = '/translation/supportedLanguages'
PROFILES_ENDPOINT = '/translation/profiles'


class TextTranslationResult(object):
    """
    Takes a text translation result (json) and makes it usable
    repr as the translation output
    """

    output = None
    detected_language = None
    detected_language_confidence = 0
    stats = {}

    def __init__(self, result: dict):
        """
        `output` is always there, but not the others
        So we try to politely set the values
        """
        self.output = result.get('output')
        self.detected_language = result.get('detectedLanguage')
        self.detected_language_confidence = result.get(
            'detectedLanguageConfidence')
        self.stats = result.get('stats')

    def __repr__(self) -> str:
        """
        The translated string
        """
        return self.output


class LanguagePairResult(object):
    """
    Takes a supported_languages result and makes it usable
    """

    source = None
    target = None
    profiles = {}

    def __init__(self, result: dict):
        """
        we try to politely set the values
        """
        self.source = result.get('source')
        self.target = result.get('target')
        self.profiles = result.get('profiles')

    def __str__(self) -> str:
        """
        A representation of the language pair : `source` → `target`
        """
        return '{} → {}'.format(self.source, self.target)


class ProfileResult(object):
    """
    Takes a profiles result and makes it usable
    """

    # pylint: disable=C0103
    id = None
    localization = {}
    name = None
    source = None
    target = None

    def __init__(self, result: dict):
        """
        we try to politely set the values
        """
        self.source = result.get('source')
        self.target = result.get('target')
        self.name = result.get('name')
        self.id = result.get('id')
        self.localization = result.get('localization')

    def __str__(self) -> str:
        """
        A string representation of the profile
        """
        return self.name


class Translation(BaseAPI):
    """
    Translation API model
    """

    input = ''
    target = ''
    source = 'auto'
    format = None
    profile = None
    with_source = None
    with_annotations = False
    with_dictionary = None
    with_corpus = None
    back_translation = False
    options = None
    encoding = 'utf-8'
    callback = None
    # pylint: disable=C0103
    id = None

    def text(self, text: str, target: str, **kwargs) -> TextTranslationResult:
        """
        Translates a single `text` into `target` language
        and returns a TextResult object

        TODO
        * handle multiple input (and loop result['outputs'])
        """
        self.input = text
        self.target = target
        self._set_attributes(**kwargs)
        response = self.post(TEXT_ENDPOINT)
        return TextTranslationResult(response['outputs'][0])

    def api_version(self) -> str:
        """
        Current version for translation apis
        """
        self._set_attributes()
        response = self.get(API_VERSION_ENDPOINT)
        return response['version']

    def supported_languages(self, source=None, target=None) -> list:
        """
        List of language pairs in which translation is supported.
        This list can be limited to a specific source language or target language.
        """
        self.source = source
        self.target = target
        results = []
        response = self.get(SUPPORTED_LANGUAGES_ENDPOINT)
        for pair in response['languagePairs']:
            results.append(LanguagePairResult(pair))
        return results

    def profiles(self, source=None, target=None, profile_id=None) -> list:
        """
        List all available profiles for translation.
        """
        self.source = source
        self.target = target
        self.id = profile_id
        results = []
        response = self.get(PROFILES_ENDPOINT)
        for profile in response['profiles']:
            results.append(ProfileResult(profile))
        return results
