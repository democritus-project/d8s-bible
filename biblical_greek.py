#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
import os
import sys
from typing import Union, List

from democritus_core import xmlRead, xml2Json, textJoin, decorators

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
# import decorators

# TODO: move this to a central location (this path exists in bible.py too)
DATA_PATH = './bible_data'


GreekWord = collections.namedtuple(
    'GreekWord', ['stem', 'ending', 'part_of_speech', 'declension', 'case', 'gender', 'number', 'stem_type']
)


# TODO: I would like to cache the data retrieved by this function
@decorators.urlEncodeFirstArg
def biblicalGreekWordInfo(word: str) -> List[GreekWord]:
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


def biblicalGreekWordStem(word: str) -> str:
    word_info = biblicalGreekWordInfo(word)
    return word_info.stem


def biblicalGreekWordLemma(word: str) -> str:
    # TODO: find the data for the nominative singular word and return that
    pass


# todo: enumerate the possible parts of speech and provide as the return types (e.g. `Union['S', 'P']`)
def biblicalGreekWordPartOfSpeech(word: str) -> str:
    word_info = biblicalGreekWordInfo(word)
    return word_info.part_of_speech


def biblicalGreekWordNumber(word: str) -> Union['singular', 'plural']:
    word_info = biblicalGreekWordInfo(word)
    return word_info.number


def biblicalGreekWordCase(word: str) -> Union['nominative', 'dative', 'genitive', 'accusative', 'vocative']:
    word_info = biblicalGreekWordInfo(word)
    return word_info.case


def biblicalGreekWordGender(word: str) -> Union['feminine', 'masculine', 'neuter']:
    word_info = biblicalGreekWordInfo(word)
    return word_info.gender


# todo: enumerate the possible declension combinations and provide as the return types (e.g. `Union['S', 'P']`)
def biblicalGreekWordDeclension(word: str) -> str:
    """."""
    word_info = biblicalGreekWordInfo(word)
    return word_info.declension


# todo: enumerate the possible stem types and provide as the return types (e.g. `Union['S', 'P']`)
def biblicalGreekWordStemType(word: str) -> str:
    """."""
    word_info = biblicalGreekWordInfo(word)
    return word_info.stem_type


# todo: write function to find details about a given verb (aspect, mode, etc...)


def bible_text_greek_xml():
    """."""
    bible = xmlRead(os.path.abspath(os.path.join(os.path.dirname(__file__), '{}/{}'.format(DATA_PATH, 'sblgnt.xml'))))
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
        if i.attrib.get('id', '').lower() == passage.lower():
            found_verse = True
        # if i has an id (which means that i is a verse) and we have already found the verse we are looking for, we have collected all the words for the desired verse and are done... we've reached the next verse.
        elif i.attrib.get('id') and found_verse:
            break
        else:
            if found_verse:
                words.append(i.text)

    text = ''.join(words)
    return text
