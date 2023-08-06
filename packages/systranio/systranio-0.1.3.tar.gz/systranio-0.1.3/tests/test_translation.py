"""
Translation unit tests
"""

import os
import unittest

import systranio
from systranio.exceptions import ParameterError, ApiKeyError, ApiFailure
from systranio.Translation import TextTranslationResult, LanguagePairResult

API_KEY = os.environ['SYSTRANIO_KEY']  # required


class TestTranslation(unittest.TestCase):
    """
    Test Translation API
    """

    def setUp(self):
        self.translation = systranio.Translation(API_KEY)

    def test_invalid_api_key(self):
        "Failure with a missing api key"
        translation = systranio.Translation('')
        with self.assertRaises(ApiKeyError):
            translation.text('pas de clé !', 'en')

    def test_invalid_parameter(self):
        "Invalid parameter added to the translation query"
        options = {'jean_michel': 'margaret'}
        with self.assertRaises(ParameterError):
            self.translation.text('cats', 'en', **options)

    def test_api_failure(self):
        "An invalid route (translation from en to en)"
        options = {'source': 'en'}
        with self.assertRaises(ApiFailure):
            self.translation.text('what ?', 'en', **options)

    def test_simple_text_translation(self):
        "A simple translation must returns something"
        options = {'source': 'en'}
        result = self.translation.text('hello', 'fr', **options)
        self.assertIsNotNone(result.output)

    def test_text_translation_returns(self):
        "A simple translation returns TextTranslationResult"
        options = {'source': 'en'}
        result = self.translation.text('hello', 'fr', **options)
        self.assertIsInstance(result, TextTranslationResult)

    def test_api_version(self):
        "api version number should be 1.0.0"
        version = self.translation.api_version()
        self.assertAlmostEqual(version, '1.0.0')

    def test_supported_languages_list(self):
        "supported_language returns a list"
        languages = self.translation.supported_languages()
        self.assertIsInstance(languages, list)

    def test_supported_languages_item(self):
        "supported_language items  a list of LanguagePairResult"
        languages = self.translation.supported_languages()
        self.assertIsInstance(languages[0], LanguagePairResult)


class TestTextTranslationResult(unittest.TestCase):
    """
    Test TextTranslationResult
    """

    def setUp(self):
        self.api_response = {
            'output': 'diffamation',
            'stats': {
                'nb_characters': 10,
                'nb_tus_failed': 0,
                'nb_tus': 1,
                'nb_tokens': 1,
                'elapsed_time': 20
            }
        }

    def test_repr(self):
        "__repr__ should be output"
        result = TextTranslationResult(self.api_response)
        self.assertEqual(str(result), result.output)


class TestLanguagePairResult(unittest.TestCase):
    """
    Test LanguagePairResult
    """

    def setUp(self):
        self.api_response = {
            "source": "nl",
            "target": "en",
            "profiles": [{
                "id": 0,
                "private": False
            }]
        }

    def test_str(self):
        "__repr__ should be output"
        result = LanguagePairResult(self.api_response)
        self.assertEqual(str(result), 'nl → en')


if __name__ == '__main__':
    unittest.main()
