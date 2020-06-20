#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .bible_references import (
    is_bible_reference,
    bible_references_find,
    bible_reference_standardize,
    bible_book_name_2_usfm,
    bible_book_name_to_osis,
)


def test_bible_book_name_to_osis_1():
    assert bible_book_name_to_osis('Genesis') == 'Gen'
    assert bible_book_name_to_osis('GENESIS') == 'Gen'
    assert bible_book_name_to_osis('genesis') == 'Gen'

    assert bible_book_name_to_osis('song of solomon') == 'Song'

    assert bible_book_name_to_osis('foo') == None


def test_bible_book_name_2_usfm_1():
    assert bible_book_name_2_usfm('Genesis') == 'GEN'
    assert bible_book_name_2_usfm('GENESIS') == 'GEN'
    assert bible_book_name_2_usfm('genesis') == 'GEN'

    assert bible_book_name_2_usfm('song of songs') == 'SNG'

    assert bible_book_name_2_usfm('foo') == None


def test_bible_reference_standardize_1():
    assert bible_reference_standardize('1 John')[0] == '1 John'

    assert bible_reference_standardize('1 John 1')[0] == '1 John 1'
    assert bible_reference_standardize('1 John1')[0] == '1 John 1'
    assert bible_reference_standardize('1 John  1')[0] == '1 John 1'

    assert bible_reference_standardize('1 John 1:1')[0] == '1 John 1:1'
    assert bible_reference_standardize('1 John1:1')[0] == '1 John 1:1'
    assert bible_reference_standardize('1 John1: 1')[0] == '1 John 1:1'
    assert bible_reference_standardize('1 John  1 : 1')[0] == '1 John 1:1'

    assert bible_reference_standardize('1 John 1:1-9')[0] == '1 John 1:1-9'
    assert bible_reference_standardize('1 John 1 : 1 - 9')[0] == '1 John 1:1-9'

    assert bible_reference_standardize('1 John 1 - 3')[0] == '1 John 1 - 3'
    assert bible_reference_standardize('1 John1-3')[0] == '1 John 1 - 3'

    assert bible_reference_standardize('1 John 1:1 - 2:3')[0] == '1 John 1:1 - 2:3'
    assert bible_reference_standardize('1 John 1:1-     2:3')[0] == '1 John 1:1 - 2:3'

    assert bible_reference_standardize('1 John 1:1 - 3')[0] == '1 John 1:1-3'
    assert bible_reference_standardize('1 John1:1-3')[0] == '1 John 1:1-3'

    assert bible_reference_standardize('1 John 1 - 3:2')[0] == '1 John 1 - 3:2'
    assert bible_reference_standardize('1 John1 -  3:2')[0] == '1 John 1 - 3:2'


def test_is_bible_reference_1():
    assert is_bible_reference('1 John')
    assert is_bible_reference('1 John 1')
    assert is_bible_reference('1 John 1:1')
    assert is_bible_reference('1 John 1:1-9')
    assert is_bible_reference('1 John 1 - 3')
    assert is_bible_reference('1 John 1:1 - 2:3')
    assert is_bible_reference('1 John 1:1 - 3')
    assert is_bible_reference('1 John 1 - 3:2')


def test_bible_references_find_1():
    results = bible_references_find('1 John')
    assert len(results) == 1
    assert results[0].book == '1 John'
    assert results[0].chapter_a == ''
    assert results[0].verse_a == ''
    assert results[0].chapter_b == ''
    assert results[0].verse_b == ''

    results = bible_references_find('1 John 1')
    assert len(results) == 1
    assert results[0].book == '1 John'
    assert results[0].chapter_a == '1'
    assert results[0].verse_a == ''
    assert results[0].chapter_b == ''
    assert results[0].verse_b == ''

    results = bible_references_find('1 John 1:2')
    assert len(results) == 1
    assert results[0].book == '1 John'
    assert results[0].chapter_a == '1'
    assert results[0].verse_a == '2'
    assert results[0].chapter_b == ''
    assert results[0].verse_b == ''

    results = bible_references_find('1 John 1:1-9')
    assert len(results) == 1
    assert results[0].book == '1 John'
    assert results[0].chapter_a == '1'
    assert results[0].verse_a == '1'
    assert results[0].chapter_b == ''
    assert results[0].verse_b == '9'

    results = bible_references_find('1 John 1:9 - 3')
    assert len(results) == 1
    assert results[0].book == '1 John'
    assert results[0].chapter_a == '1'
    assert results[0].verse_a == '9'
    assert results[0].chapter_b == '3'
    assert results[0].verse_b == ''

    results = bible_references_find('1 John 1:1-2:9')
    assert len(results) == 1
    assert results[0].book == '1 John'
    assert results[0].chapter_a == '1'
    assert results[0].verse_a == '1'
    assert results[0].chapter_b == '2'
    assert results[0].verse_b == '9'

    results = bible_references_find('1 John 1 - 3')
    assert len(results) == 1
    assert results[0].book == '1 John'
    assert results[0].chapter_a == '1'
    assert results[0].verse_a == ''
    assert results[0].chapter_b == '3'
    assert results[0].verse_b == ''

    results = bible_references_find('1 John 1:1 - 3')
    assert len(results) == 1
    assert results[0].book == '1 John'
    assert results[0].chapter_a == '1'
    assert results[0].verse_a == '1'
    assert results[0].chapter_b == ''
    assert results[0].verse_b == '3'

    results = bible_references_find('1 John 1 - 3:2')
    assert len(results) == 1
    assert results[0].book == '1 John'
    assert results[0].chapter_a == '1'
    assert results[0].verse_a == ''
    assert results[0].chapter_b == '3'
    assert results[0].verse_b == '2'

    results = bible_references_find('Ecclesiastes 2:17-26')
    assert len(results) == 1
    assert results[0].book == 'Ecclesiastes'
    assert results[0].chapter_a == '2'
    assert results[0].verse_a == '17'
    assert results[0].chapter_b == ''
    assert results[0].verse_b == '26'

    # handle books that only have one chapter
    results = bible_references_find('Jude 3 - 7')
    assert len(results) == 1
    assert results[0].book == 'Jude'
    assert results[0].chapter_a == '1'
    assert results[0].verse_a == '3'
    assert results[0].chapter_b == '1'
    assert results[0].verse_b == '7'
