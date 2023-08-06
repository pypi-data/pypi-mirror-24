import requests
import json

BASE_URL = 'https://www.deepl.com/jsonrpc'

LANGUAGES = {
    'DE': 'German',
    'EN': 'English',
    'FR': 'French',
    'ES': 'Spanish',
    'IT': 'Italian',
    'NL': 'Dutch',
    'PL': 'Polish'
}


class TranslationError(Exception):
    def __init__(self, message, errors):
        super(TranslationError, self).__init__(message)
        self.errors = errors


def translate(text, from_lang, to_lang):
    if text is None:
        raise TranslationError('Text can\'t be None.', {})
    if to_lang not in LANGUAGES.keys():
        raise TranslationError('Language {} not available.'.format(to_lang), {})
    if from_lang is not None and from_lang not in LANGUAGES.keys():
        raise TranslationError('Language {} not available.'.format(from_lang), {})

    parameters = {
        'jsonrpc': '2.0',
        'method': 'LMT_handle_jobs',
        'params': {
            'jobs': [
                {
                    'kind':'default',
                    'raw_en_sentence': text
                }
            ],
            'lang': {
                'user_preferred_langs': [
                    from_lang,
                    to_lang
                ],
                'source_lang_user_selected': from_lang,
                'target_lang': to_lang
            },
            'priority': -1
        },
    }

    response = json.loads(requests.post(BASE_URL, json=parameters).text)

    translations = response['result']['translations']

    if len(translations) == 0 or translations[0]['beams'] is None or translations[0]['beams'][0]['postprocessed_sentence'] is None:
        raise TranslationError('No translations found.', {})

    return translations[0]['beams'][0]['postprocessed_sentence']