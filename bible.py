#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from democritus_core import xmlRead, xml2String, metaOutput

DATA_PATH = './bible_data'


def bibleXml():
    """Get the xml data for the Bible."""
    bible = xmlRead(os.path.abspath(os.path.join(os.path.dirname(__file__), '{}/{}'.format(DATA_PATH, 'nasb.xml'))))
    return bible


def bibleBook(book):
    """Get the xml data for the given book of the Bible."""
    from strings import lowercase

    bible_xml = bibleXml()
    for book_xml in bible_xml:
        if lowercase(book_xml.attrib['name']) == lowercase(book):
            return book_xml
    metaOutput('Unable to find the book named "{}" in the bible'.format(book))


def bibleJson():
    """Get json data for the bible."""
    from xml_data import xml2Json

    bible_xml = bibleXml()
    bible_json = xml2Json(bible_xml)
    return bible_json


def bibleBooks():
    """Get a list of the books in the Bible."""
    bible_xml = bibleXml()
    return [book_xml.attrib['name'] for book_xml in bible_xml]


def bibleBookString(book):
    """Get the string for the given book of the Bible."""
    return xml2String(bibleBook(book))


def bibleBookChapterCount(book):
    """Get the number of chapters in the given book."""
    return len(bibleBook(book))


def bibleChapterCount():
    """Return the number of chapters in the Bible."""
    chapters = 0
    for book in bibleBooks():
        chapters += bibleBookChapterCount(book)
    return chapters


def bibleBookChapter(book, chapter_number):
    """Get the xml data for the given chapter of the given book."""
    book_xml = bibleBook(book)
    for chapter_xml in book_xml:
        if chapter_xml.attrib['name'] == str(chapter_number):
            return chapter_xml
    metaOutput('Unable to find data for chapter {} in {}'.format(chapter_number, book))


def bibleBookChapterString(book, chapter_number):
    """Get the string for the given chapter in the given book."""
    return xml2String(bibleBookChapter(book, chapter_number))


def bibleBookChapterVerses(book, chapter_number):
    """Get the verses in the given chapter."""
    book_xml = bibleBook(book)
    return book_xml[chapter_number - 1]


def bibleBookChapterVerseCount(book, chapter_number):
    """Get the number of verses in the given chapter."""
    book_xml = bibleBook(book)
    return len(book_xml[chapter_number - 1])


def bibleBookVerseCount(book):
    """Get the number of verses in the given book."""
    verses_count = 0
    for chapter in range(1, bibleBookChapterCount(book) + 1):
        verses_count += bibleBookChapterVerses(book, chapter)
    return verses_count


def bibleBookWordCountByChapter(book, word=None):
    """Find the count of the given word in the given book. If no word is given, the function will return the number of words in each chapter."""
    from nlp import wordsCount, wordCount

    data = {}

    for i in range(0, bibleBookChapterCount(book)):
        chapter_number = i + 1
        chapter_string = bibleBookChapterString(book, chapter_number)

        if word:
            data[chapter_number] = wordCount(chapter_string, word)
        else:
            data[chapter_number] = wordsCount(chapter_string)

    return data


def bibleBookWordCount(book, word=None):
    """Find the number of words in the book. If a word is given as an argument, this function will return the number of times that word occurs in the given book."""
    from nlp import wordsCount, wordCount

    book_string = bibleBookString(book)

    if word:
        return wordCount(book_string, word)
    else:
        return wordsCount(book_string)


def bibleWordCountByBook(word=None):
    """Find the count of the given word in the bible. If no word is given, the function will return the number of words in each book."""
    from nlp import wordsCount, wordCount

    data = {}

    for book in bibleBooks():
        book_string = bibleBookString(book)

        if word:
            data[book] = wordCount(book_string, word)
        else:
            data[book] = wordsCount(book_string)

    return data


def bibleRateToFinish(days=365):
    """Return the number of chapters you would have to read every day to finish the Bible in the given number of days."""
    return bibleChapterCount() / days


def biblePassageGreek(bible_passage: str):
    pass


# TODO: write function to find all refs to a given word in a given range/text
# TODO: write function to produce a concordance of a given word


# TODO: note sure what this code is all about, but it may be useful... I think the basic gist is that bible data should come back as json rather than xml:

# for book in bibleBooks():
#     print(book)
#     book_xml = bibleBook(book)
#     book_xml_string = xml2String(book_xml)
#     book_json = xml2Json(book_xml_string)
#     print(book_json)
#     break
