#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from biblical_greek import biblical_greek_word_info, bible_text_greek


def test_biblical_greek_word_info_1():
    results = biblical_greek_word_info('φαῦλον')
    print(results)
    assert len(results) == 9
    assert results[0].stem == 'φαῡλ'
    assert results[0].ending == 'ον'
    assert results[0].part_of_speech == 'adjective'
    assert results[0].declension == '1st & 2nd'
    assert results[0].case == 'accusative'
    assert results[0].gender == 'masculine'
    assert results[0].number == 'singular'
    assert results[0].stem_type == 'os_h_on'

    results = biblical_greek_word_info('φαῦλος')
    print(results)
    assert len(results) == 3
    assert results[0].stem == 'φαῡλ'
    assert results[0].ending == 'ος'
    assert results[0].part_of_speech == 'adjective'
    assert results[0].declension == '1st & 2nd'
    assert results[0].case == 'nominative'
    assert results[0].gender == 'masculine'
    assert results[0].number == 'singular'
    assert results[0].stem_type == 'os_h_on'


def test_biblical_greek_word_info_bad_input():
    results = biblical_greek_word_info('foo')
    assert len(results) == 0


def test_bible_text_greek_1():
    results = bible_text_greek('john 1:2')
    assert results == 'οὗτος ἦν ἐν ἀρχῇ πρὸς τὸν θεόν.  '

    results = bible_text_greek('John 1:2')
    assert results == 'οὗτος ἦν ἐν ἀρχῇ πρὸς τὸν θεόν.  '
