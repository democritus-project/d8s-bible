#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyparsing import Or, Word, nums
from bible import bibleBooks

bible_book_grammar = Or(bibleBooks())
bible_verse_grammar = bible_chapter_grammar = Word(nums)
bible_location_grammar = (
    bible_chapter_grammar('chapter') + Word(':') + bible_verse_grammar('verse')
    | bible_chapter_grammar('chapter')
    | bible_verse_grammar('verse')
)
bible_location_range_grammar = bible_location_grammar('location_a') + Word('-') + bible_location_grammar('location_b')
bible_reference_grammar = (
    bible_book_grammar('book') + bible_location_range_grammar('location_range')
    | bible_book_grammar('book') + bible_location_grammar('location')
    | bible_book_grammar('book')
)
