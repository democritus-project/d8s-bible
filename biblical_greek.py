#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
import os
import sys
from typing import Union, List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
import decorators


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
