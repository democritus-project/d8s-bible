#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .bible_references import (
    isBibleReference,
    bibleReferencesFind,
    bibleReferenceStandardize,
    bibleBookName2Usfm,
    bibleBookName2Osis,
)


def test_bibleBookName2Osis_1():
    assert bibleBookName2Osis('Genesis') == 'Gen'
    assert bibleBookName2Osis('GENESIS') == 'Gen'
    assert bibleBookName2Osis('genesis') == 'Gen'

    assert bibleBookName2Osis('song of solomon') == 'Song'

    assert bibleBookName2Osis('foo') == None


def test_bibleBookName2Usfm_1():
    assert bibleBookName2Usfm('Genesis') == 'GEN'
    assert bibleBookName2Usfm('GENESIS') == 'GEN'
    assert bibleBookName2Usfm('genesis') == 'GEN'

    assert bibleBookName2Usfm('song of songs') == 'SNG'

    assert bibleBookName2Usfm('foo') == None


def test_bibleReferenceStandardize_1():
    assert bibleReferenceStandardize('1 John')[0] == '1 John'

    assert bibleReferenceStandardize('1 John 1')[0] == '1 John 1'
    assert bibleReferenceStandardize('1 John1')[0] == '1 John 1'
    assert bibleReferenceStandardize('1 John  1')[0] == '1 John 1'

    assert bibleReferenceStandardize('1 John 1:1')[0] == '1 John 1:1'
    assert bibleReferenceStandardize('1 John1:1')[0] == '1 John 1:1'
    assert bibleReferenceStandardize('1 John1: 1')[0] == '1 John 1:1'
    assert bibleReferenceStandardize('1 John  1 : 1')[0] == '1 John 1:1'

    assert bibleReferenceStandardize('1 John 1:1-9')[0] == '1 John 1:1-9'
    assert bibleReferenceStandardize('1 John 1 : 1 - 9')[0] == '1 John 1:1-9'

    assert bibleReferenceStandardize('1 John 1 - 3')[0] == '1 John 1 - 3'
    assert bibleReferenceStandardize('1 John1-3')[0] == '1 John 1 - 3'

    assert bibleReferenceStandardize('1 John 1:1 - 2:3')[0] == '1 John 1:1 - 2:3'
    assert bibleReferenceStandardize('1 John 1:1-     2:3')[0] == '1 John 1:1 - 2:3'

    assert bibleReferenceStandardize('1 John 1:1 - 3')[0] == '1 John 1:1-3'
    assert bibleReferenceStandardize('1 John1:1-3')[0] == '1 John 1:1-3'

    assert bibleReferenceStandardize('1 John 1 - 3:2')[0] == '1 John 1 - 3:2'
    assert bibleReferenceStandardize('1 John1 -  3:2')[0] == '1 John 1 - 3:2'


def test_isBibleReference_1():
    assert isBibleReference('1 John')
    assert isBibleReference('1 John 1')
    assert isBibleReference('1 John 1:1')
    assert isBibleReference('1 John 1:1-9')
    assert isBibleReference('1 John 1 - 3')
    assert isBibleReference('1 John 1:1 - 2:3')
    assert isBibleReference('1 John 1:1 - 3')
    assert isBibleReference('1 John 1 - 3:2')


def test_bibleReferencesFind_1():
    results = bibleReferencesFind('1 John')
    assert len(results) == 1
    assert results[0].book == '1 John'
    assert results[0].chapter_a == ''
    assert results[0].verse_a == ''
    assert results[0].chapter_b == ''
    assert results[0].verse_b == ''

    results = bibleReferencesFind('1 John 1')
    assert len(results) == 1
    assert results[0].book == '1 John'
    assert results[0].chapter_a == '1'
    assert results[0].verse_a == ''
    assert results[0].chapter_b == ''
    assert results[0].verse_b == ''

    results = bibleReferencesFind('1 John 1:2')
    assert len(results) == 1
    assert results[0].book == '1 John'
    assert results[0].chapter_a == '1'
    assert results[0].verse_a == '2'
    assert results[0].chapter_b == ''
    assert results[0].verse_b == ''

    results = bibleReferencesFind('1 John 1:1-9')
    assert len(results) == 1
    assert results[0].book == '1 John'
    assert results[0].chapter_a == '1'
    assert results[0].verse_a == '1'
    assert results[0].chapter_b == ''
    assert results[0].verse_b == '9'

    results = bibleReferencesFind('1 John 1:9 - 3')
    assert len(results) == 1
    assert results[0].book == '1 John'
    assert results[0].chapter_a == '1'
    assert results[0].verse_a == '9'
    assert results[0].chapter_b == '3'
    assert results[0].verse_b == ''

    results = bibleReferencesFind('1 John 1:1-2:9')
    assert len(results) == 1
    assert results[0].book == '1 John'
    assert results[0].chapter_a == '1'
    assert results[0].verse_a == '1'
    assert results[0].chapter_b == '2'
    assert results[0].verse_b == '9'

    results = bibleReferencesFind('1 John 1 - 3')
    assert len(results) == 1
    assert results[0].book == '1 John'
    assert results[0].chapter_a == '1'
    assert results[0].verse_a == ''
    assert results[0].chapter_b == '3'
    assert results[0].verse_b == ''

    results = bibleReferencesFind('1 John 1:1 - 3')
    assert len(results) == 1
    assert results[0].book == '1 John'
    assert results[0].chapter_a == '1'
    assert results[0].verse_a == '1'
    assert results[0].chapter_b == ''
    assert results[0].verse_b == '3'

    results = bibleReferencesFind('1 John 1 - 3:2')
    assert len(results) == 1
    assert results[0].book == '1 John'
    assert results[0].chapter_a == '1'
    assert results[0].verse_a == ''
    assert results[0].chapter_b == '3'
    assert results[0].verse_b == '2'

    results = bibleReferencesFind('Ecclesiastes 2:17-26')
    assert len(results) == 1
    assert results[0].book == 'Ecclesiastes'
    assert results[0].chapter_a == '2'
    assert results[0].verse_a == '17'
    assert results[0].chapter_b == ''
    assert results[0].verse_b == '26'

    # handle books that only have one chapter
    results = bibleReferencesFind('Jude 3 - 7')
    assert len(results) == 1
    assert results[0].book == 'Jude'
    assert results[0].chapter_a == '1'
    assert results[0].verse_a == '3'
    assert results[0].chapter_b == '1'
    assert results[0].verse_b == '7'
