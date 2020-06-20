#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
import os
import sys
from typing import Union, List

from democritus_core import xml_read, decorators

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
# import decorators

# TODO: move this to a central location (this path exists in bible.py too)
DATA_PATH = './bible_data'


GreekWord = collections.namedtuple(
    'GreekWord', ['stem', 'ending', 'part_of_speech', 'declension', 'case', 'gender', 'number', 'stem_type']
)


# TODO: I would like to cache the data retrieved by this function
@decorators.url_encode_first_arg
def biblical_greek_word_info(word: str) -> List[GreekWord]:
    from networking import get

    word_data = []

    url = f'http://services.perseids.org/bsp/morphologyservice/analysis/word?lang=grc&engine=morpheusgrc&word={word}'
    json_response = get(url)

    if json_response['RDF']['Annotation'].get('Body'):
        for entry in json_response['RDF']['Annotation']['Body']['rest']['entry']['infl']:

            new_word_data = GreekWord(
                stem=entry['term']['stem']['$'],
                ending=entry['term']['suff']['$'],
                part_of_speech=entry['pofs']['$'],
                declension=entry['decl']['$'],
                case=entry['case']['$'],
                gender=entry['gend']['$'],
                number=entry['num']['$'],
                stem_type=entry['stemtype']['$'],
            )
            word_data.append(new_word_data)
    else:
        message = f'No data found for the word: "{word}"'
        print(message)

    return word_data


def biblical_greek_word_stem(word: str) -> str:
    word_info = biblical_greek_word_info(word)
    return word_info.stem


def biblical_greek_word_lemma(word: str) -> str:
    # TODO: find the data for the nominative singular word and return that
    pass


# todo: enumerate the possible parts of speech and provide as the return types (e.g. `Union['S', 'P']`)
def biblical_greek_word_part_of_speech(word: str) -> str:
    word_info = biblical_greek_word_info(word)
    return word_info.part_of_speech


def biblical_greek_word_number(word: str) -> Union['singular', 'plural']:
    word_info = biblical_greek_word_info(word)
    return word_info.number


def biblical_greek_word_case(word: str) -> Union['nominative', 'dative', 'genitive', 'accusative', 'vocative']:
    word_info = biblical_greek_word_info(word)
    return word_info.case


def biblical_greek_word_gender(word: str) -> Union['feminine', 'masculine', 'neuter']:
    word_info = biblical_greek_word_info(word)
    return word_info.gender


# todo: enumerate the possible declension combinations and provide as the return types (e.g. `Union['S', 'P']`)
def biblical_greek_word_declension(word: str) -> str:
    """."""
    word_info = biblical_greek_word_info(word)
    return word_info.declension


# todo: enumerate the possible stem types and provide as the return types (e.g. `Union['S', 'P']`)
def biblical_greek_word_stem_type(word: str) -> str:
    """."""
    word_info = biblical_greek_word_info(word)
    return word_info.stem_type


# todo: write function to find details about a given verb (aspect, mode, etc...)


def bible_text_greek_xml():
    """."""
    bible = xml_read(os.path.abspath(os.path.join(os.path.dirname(__file__), '{}/{}'.format(DATA_PATH, 'sblgnt.xml'))))
    return bible


# TODO: eventually, I'd like to be able to handle passages like "Romans 1:1-18" and return the data for all of those verses, but I can't do that yet.
# TODO: standardize the passage argument
def bible_text_greek(passage: str):
    """Get the Greek text for the given bible passage."""
    bible_xml = bible_text_greek_xml()
    found_verse = False
    text = None
    words = []

    for i in bible_xml.iter():
        if found_verse:
            # if i is a tag containing words/markings for the verse, add it
            if i.tag in ('prefix', 'w', 'suffix'):
                words.append(i.text)
            # if i is not a tag containing words/markings for the verse, we are done collecting data for the verse
            else:
                break
        else:
            if i.attrib.get('id', '').lower() == passage.lower():
                found_verse = True

    if found_verse:
        text = ''.join(words)
    return text
