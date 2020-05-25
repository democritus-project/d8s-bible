#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from biblical_greek import biblicalGreekWordInfo


def test_biblicalGreekWordInfo_1():
    results = biblicalGreekWordInfo('φαῦλον')
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

    results = biblicalGreekWordInfo('φαῦλος')
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


def test_biblicalGreekWordInfo_bad_input():
    results = biblicalGreekWordInfo('foo')
    assert len(results) == 0
