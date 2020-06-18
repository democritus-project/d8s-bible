#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from democritus_core import xml_read, xml_to_string, lowercase, xml_to_json

DATA_PATH = './bible_data'


def bible_xml():
    """Get the xml data for the Bible."""
    bible = xml_read(os.path.abspath(os.path.join(os.path.dirname(__file__), '{}/{}'.format(DATA_PATH, 'nasb.xml'))))
    return bible


# TODO: RETURN JSON RATHER THAN XML (AND PROBABLY INCLUDE A REFERENCE TO JSON IN THE FUNCTION NAME (E.G. bible_book_json ))
def bible_book(book):
    """Get the xml data for the given book of the Bible."""
    bible_xml = bible_xml()
    for book_xml in bible_xml:
        if lowercase(book_xml.attrib['bname']) == lowercase(book):
            return book_xml
    print('Unable to find the book named "{}" in the bible'.format(book))


# def bible_book_json
# def bible_book_text
# def bible_book_chapter_json
# def bible_book_chapter_text
# def bible_book_chapter_verse_json
# def bible_book_chapter_verse_text


def bible_json():
    """Get json data for the bible."""
    bible_xml_data = bible_xml()
    bible_json_data = xml_to_json(bible_xml_data)
    return bible_json_data


def bible_books():
    """Get a list of the books in the Bible."""
    bible_xml_data = bible_xml()
    return [book_xml.attrib['bname'] for book_xml in bible_xml_data]


def bible_book_string(book):
    """Get the string for the given book of the Bible."""
    return xml_to_string(bible_book(book))


def bible_book_chapter_count(book):
    """Get the number of chapters in the given book."""
    return len(bible_book(book))


def bible_chapter_count():
    """Return the number of chapters in the Bible."""
    chapters = 0
    for book in bible_books():
        chapters += bible_book_chapter_count(book)
    return chapters


def bible_book_chapter(book, chapter_number):
    """Get the xml data for the given chapter of the given book."""
    book_xml = bible_book(book)
    for chapter_xml in book_xml:
        if chapter_xml.attrib['name'] == str(chapter_number):
            return chapter_xml
    print('Unable to find data for chapter {} in {}'.format(chapter_number, book))


def bible_book_chapter_string(book, chapter_number):
    """Get the string for the given chapter in the given book."""
    return xml_to_string(bible_book_chapter(book, chapter_number))


def bible_book_chapter_verses(book, chapter_number):
    """Get the verses in the given chapter."""
    # todo: convert chapter_number to an int
    # todo: I don't think this function is working properly
    book_xml = bible_book(book)
    return book_xml[chapter_number - 1]


def bible_book_chapter_verse_count(book, chapter_number):
    """Get the number of verses in the given chapter."""
    book_xml = bible_book(book)
    return len(book_xml[chapter_number - 1])


def bible_book_verse_count(book):
    """Get the number of verses in the given book."""
    verses_count = 0
    for chapter in range(1, bible_book_chapter_count(book) + 1):
        verses_count += bible_book_chapter_verses(book, chapter)
    return verses_count


def bible_book_word_count_by_chapter(book, word=None):
    """Find the count of the given word in the given book. If no word is given, the function will return the number of words in each chapter."""
    from nlp import wordsCount, wordCount

    data = {}

    for i in range(0, bible_book_chapter_count(book)):
        chapter_number = i + 1
        chapter_string = bible_book_chapter_string(book, chapter_number)

        if word:
            data[chapter_number] = wordCount(chapter_string, word)
        else:
            data[chapter_number] = wordsCount(chapter_string)

    return data


def bible_book_word_count(book, word=None):
    """Find the number of words in the book. If a word is given as an argument, this function will return the number of times that word occurs in the given book."""
    from nlp import wordsCount, wordCount

    book_string = bible_book_string(book)

    if word:
        return wordCount(book_string, word)
    else:
        return wordsCount(book_string)


def bible_word_count_by_book(word=None):
    """Find the count of the given word in the bible. If no word is given, the function will return the number of words in each book."""
    from nlp import wordsCount, wordCount

    data = {}

    for book in bible_books():
        book_string = bible_book_string(book)

        if word:
            data[book] = wordCount(book_string, word)
        else:
            data[book] = wordsCount(book_string)

    return data


def bible_rate_to_finish(days=365):
    """Return the number of chapters you would have to read every day to finish the Bible in the given number of days."""
    return bible_chapter_count() / days


def bible_passage_greek(bible_passage: str):
    pass


# TODO: write function to find all refs to a given word in a given range/text
# TODO: write function to produce a concordance of a given word


# TODO: note sure what this code is all about, but it may be useful... I think the basic gist is that bible data should come back as json rather than xml:

# for book in bible_books():
#     print(book)
#     book_xml = bible_book(book)
#     book_xml_string = xml_to_string(book_xml)
#     book_json = xml_to_json(book_xml_string)
#     print(book_json)
#     break
