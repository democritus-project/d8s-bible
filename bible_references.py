#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections

from democritus_core import (
    typings,
    pyparsingParseResultGetTokenDict,
    textJoin,
    templateRender,
    html2Json,
    get,
    lowercase,
)


# TODO: update this such that the chapter and verses are optional
BiblePassage = collections.namedtuple('BiblePassage', ['book', 'chapter_a', 'verse_a', 'chapter_b', 'verse_b'])
BibleRange = collections.namedtuple('BibleRange', ['passage_a', 'passage_b'])


def isBibleReference(possible_bible_reference: str) -> bool:
    """."""
    references = bibleReferencesFind(possible_bible_reference)
    if references and len(references) == 1:
        return True
    else:
        return False


def bibleReferenceStandardize(bible_reference: str) -> typings.ListString:
    """."""
    standardized_references = []

    references = bibleReferencesFind(bible_reference)

    for ref in references:
        template = '{{ book }}{% if chapter_a %} {{ chapter_a }}{% endif %}{% if verse_a %}{% if chapter_a %}:{% else %} {% endif %}{{ verse_a }}{% endif %}{% if chapter_b or verse_b %}{% if chapter_b %} {% endif %}-{% if chapter_b %} {% endif %}{% endif %}{% if chapter_b %}{{ chapter_b }}{% endif %}{% if verse_b %}{% if chapter_b %}:{% endif %}{{ verse_b }}{% endif %}'
        standardized_ref = templateRender(template, **ref._asdict())
        standardized_references.append(standardized_ref)

    return standardized_references


# TODO: set the return type to a list of bible reference objects
def bibleReferencesFind(text: str):
    from bible_references_grammars import bible_reference_grammar

    references = bible_reference_grammar.searchString(text)

    bible_references = []

    # NOTE: throughout the code below, the `.tup[0]` business makes sure that we are getting the value of each element of the result as a string

    for reference in references:
        # TODO: there is probably a better way to access the _ParseResults__tokdict, but this works for now
        dict_reference = pyparsingParseResultGetTokenDict(reference)

        book = dict_reference['book'][0].tup[0]

        chapter_a = ''
        chapter_b = ''
        verse_a = ''
        verse_b = ''

        # define some properties that are used later
        ref_has_two_chapters = len(dict_reference.get('chapter', [])) == 2
        ref_has_one_verse = len(dict_reference.get('verse', [])) == 1
        ref_has_two_verses = len(dict_reference.get('verse', [])) == 2
        ref_has_location_range = any(reference.location_range)

        if dict_reference.get('verse'):
            ref_first_verse = dict_reference['verse'][0].tup[0]
        else:
            ref_first_verse = ''

        ref_first_verse_in_location_a = ''.join(reference.location_a).endswith(ref_first_verse)

        # identify/validate the chapters
        if dict_reference.get('chapter'):
            chapter_a = dict_reference['chapter'][0].tup[0]

            if ref_has_two_chapters:
                second_chapter = dict_reference['chapter'][1].tup[0]

                # if there is only one verse, we need to disambiguate whether or not the value parsed as the second_chapter is a chapter or a verse (e.g. the '9' in '1 John 1:1-9')
                if ref_has_one_verse:
                    # if this second_chapter is greater than the previous verse (and the previous verse has already been used), we are going to assume this number is another verse
                    second_chapter_greater_than_previous_verse = int(second_chapter) > int(ref_first_verse)
                    if second_chapter_greater_than_previous_verse and ref_first_verse_in_location_a:
                        verse_b = second_chapter
                        # TODO: check to see if the verse is valid (if the given book and the given chapter actually has that many verses)
                    else:
                        chapter_b = second_chapter
                else:
                    chapter_b = second_chapter

        # identify/validate the verses
        if dict_reference.get('verse'):
            if ref_has_two_verses:
                verse_a = dict_reference['verse'][0].tup[0]
                verse_b = dict_reference['verse'][1].tup[0]
            else:
                # if the reference has a location range and the only verse found in the reference does not occur in the location_a, we can assume the verse is the second verse, belonging with the second location
                if ref_has_location_range and not ref_first_verse_in_location_a:
                    verse_b = dict_reference['verse'][0].tup[0]
                else:
                    verse_a = dict_reference['verse'][0].tup[0]

        new_reference = BiblePassage(
            book=book, chapter_a=chapter_a, chapter_b=chapter_b, verse_a=verse_a, verse_b=verse_b,
        )
        bible_references.append(new_reference)

    return bible_references


# TODO: in the functions below, there are different names for the same books (e.g. song of songs vs. song of solomon)


BIBLE_BOOK_ENGLISH_NAMES_2_OSIS_MAPPING = {
    'genesis': 'Gen',
    'exodus': 'Exod',
    'leviticus': 'Lev',
    'numbers': 'Num',
    'deuteronomy': 'Deut',
    'joshua': 'Josh',
    'judges': 'Judg',
    'ruth': 'Ruth',
    '1 samuel': '1Sam',
    '2 samuel': '2Sam',
    '1 kings': '1Kgs',
    '2 kings': '2Kgs',
    '1 chronicles': '1Chr',
    '2 chronicles': '2Chr',
    'ezra': 'Ezra',
    'nehemiah': 'Neh',
    'esther[6]': 'Esth',
    'job': 'Job',
    'psalms': 'Ps',
    'proverbs': 'Prov',
    'ecclesiastes': 'Eccl',
    'song of solomon': 'Song',
    'isaiah': 'Isa',
    'jeremiah': 'Jer',
    'lamentations': 'Lam',
    'ezekiel': 'Ezek',
    'daniel': 'Dan',
    'hosea': 'Hos',
    'joel': 'Joel',
    'amos': 'Amos',
    'obadiah': 'Obad',
    'jonah': 'Jonah',
    'micah': 'Mic',
    'nahum': 'Nah',
    'habakkuk': 'Hab',
    'zephaniah': 'Zeph',
    'haggai': 'Hag',
    'zechariah': 'Zech',
    'malachi': 'Mal',
    'matthew': 'Matt',
    'mark': 'Mark',
    'luke': 'Luke',
    'john': 'John',
    'acts': 'Acts',
    'romans': 'Rom',
    '1 corinthians': '1Cor',
    '2 corinthians': '2Cor',
    'galatians': 'Gal',
    'ephesians': 'Eph',
    'philippians': 'Phil',
    'colossians': 'Col',
    '1 thessalonians': '1Thess',
    '2 thessalonians': '2Thess',
    '1 timothy': '1Tim',
    '2 timothy': '2Tim',
    'titus': 'Titus',
    'philemon': 'Phlm',
    'hebrews': 'Heb',
    'james': 'Jas',
    '1 peter': '1Pet',
    '2 peter': '2Pet',
    '1 john': '1John',
    '2 john': '2John',
    '3 john': '3John',
    'jude': 'Jude',
    'revelation': 'Rev',
    # 'tobit': 'Tob',
    # 'judith': 'Jdt',
    # 'greek esther': 'EsthGr',
    # 'additions to esther': 'AddEsth',
    # 'wisdom': 'Wis',
    # 'sirach prologue': 'SirP',
    # 'sirach': 'Sir',
    # 'baruch': 'Bar',
    # 'letter of jeremiah': 'EpJer',
    # 'greek daniel': 'DanGr',
    # 'additions to daniel': 'AddDan',
    # 'prayer of azariah': 'PrAzar',
    # 'susanna': 'Sus',
    # 'bel and the dragon': 'Bel',
    # '1 maccabees': '1Macc',
    # '2 maccabees': '2Macc',
    # '3 maccabees': '3Macc',
    # '4 maccabees': '4Macc',
    # 'prayer of manasseh': 'PrMan',
    # '1 esdras': '1Esd',
    # '2 esdras': '2Esd',
    # 'psalm 151': 'AddPs',
    # 'odes': 'Odes',
    # 'psalms of solomon': 'PssSol',
    # 'joshua a': 'JoshA',
    # 'judges b': 'JudgB',
    # 'tobit s': 'TobS',
    # 'susanna θ': 'SusTh',
    # 'daniel θ': 'DanTh',
    # 'bel and the dragon θ': 'BelTh',
    # 'epistle to the laodiceans': 'EpLao',
    # '5 ezra': '5Ezra',
    # '4 ezra': '4Ezra',
    # '6 ezra': '6Ezra',
    # 'prayer of solomon': 'PrSol',
    # 'prayer of jeremiah': 'PrJer',
    # '1 enoch': '1En',
    # 'jubilees': 'Jub',
    # '4 baruch': '4Bar',
    # '1 meqabyan': '1Meq',
    # '2 meqabyan': '2Meq',
    # '3 meqabyan': '3Meq',
    # 'reproof': 'Rep',
    # 'additions to jeremiah': 'AddJer',
    # 'pseudo-josephus': 'PsJos',
    # 'epistle of the corinthians to paul': 'EpCorPaul',
    # '3 corinthians': '3Cor',
    # 'words of sirach': 'WSir',
    # 'prayer of euthalius': 'PrEuth',
    # 'dormition of john': 'DormJohn',
    # 'joseph and asenath': 'JosAsen',
    # 'testaments of the twelve patriarchs (composed of:)': 'T12Patr',
    # 'testament of asher': 'T12Patr.TAsh',
    # 'testament of benjamin': 'T12Patr.TBenj',
    # 'testament of dan': 'T12Patr.TDan',
    # 'testament of gad': 'T12Patr.TGad',
    # 'testament of issachar': 'T12Patr.TIss',
    # 'testament of joseph': 'T12Patr.TJos',
    # 'testament of judah': 'T12Patr.TJud',
    # 'testament of levi': 'T12Patr.TLevi',
    # 'testament of naphtali': 'T12Patr.TNaph',
    # 'testament of reuben': 'T12Patr.TReu',
    # 'testament of simeon': 'T12Patr.TSim',
    # 'testament of zebulun': 'T12Patr.TZeb',
    # '2 baruch': '2Bar',
    # 'letter of baruch': 'EpBar',
    # 'additional syriac psalms': '5ApocSyrPss',
    # 'josephus\' jewish war vi': 'JosephusJWvi',
    # '1 clement': '1Clem',
    # '2 clement': '2Clem',
    # 'ignatius to the ephesians': 'IgnEph',
    # 'ignatius to the magnesians': 'IgnMagn',
    # 'ignatius to the trallians': 'IgnTrall',
    # 'ignatius to the romans': 'IgnRom',
    # 'ignatius to the philadelphians': 'IgnPhld',
    # 'ignatius to the smyrnaeans': 'IgnSmyrn',
    # 'ignatius to polycarp': 'IgnPol',
    # 'polycarp to the philippians': 'PolPhil',
    # 'martyrdom of polycarp': 'MartPol',
    # 'didache': 'Did',
    # 'barnabas': 'Barn',
    # 'shepherd of hermas (comprised of:)': 'Herm',
    # 'shepherd of hermas, mandates': 'Herm.Mand',
    # 'shepherd of hermas, similitudes': 'Herm.Sim',
    # 'shepherd of hermas, visions': 'Herm.Vis',
    # 'diognetus': 'Diogn',
    # 'apostles\' creed': 'AposCreed',
    # 'fragments of papias': 'PapFrag',
    # 'reliques of the elders': 'RelElders',
    # 'fragment of quadratus': 'QuadFrag',
    # 'diatessaron': 'TatDiat',
    # 'metrical psalms': 'PsMet',
}


def bibleBookNamesEnglish2OsisMappings():
    """Get data from the first table in https://wiki.crosswire.org/OSIS_Book_Abbreviations and return a mapping from english names to OSIS names."""
    url = 'https://wiki.crosswire.org/OSIS_Book_Abbreviations'
    tables = html2Json(get(url), convert_only_tables=True)

    assert len(tables) == 1
    table = tables[0]

    english_to_osis_book_name_mappings = {
        i['Book Name\n'].strip(' †\n').lower(): i['osisID\n'].strip(' †\n')
        for i in t
        if i.get('Book Name\n') and i.get('osisID\n')
    }

    return english_to_osis_book_name_mappings


def bibleBookName2Osis(book_name: str) -> typings.StringOrNone:
    """Convert the given book name (as either the english name or USFM format) into OSIS.

    Helpful sources: [https://wiki.crosswire.org/OSIS_Book_Abbreviations]"""
    # TODO: handle book_name's which are in USFM format

    osis_book_name = BIBLE_BOOK_ENGLISH_NAMES_2_OSIS_MAPPING.get(lowercase(book_name))
    return osis_book_name


BIBLE_BOOK_ENGLISH_NAMES_2_USFM_MAPPING = {
    'genesis': 'GEN',
    'exodus': 'EXO',
    'leviticus': 'LEV',
    'numbers': 'NUM',
    'deuteronomy': 'DEU',
    'joshua': 'JOS',
    'judges': 'JDG',
    'ruth': 'RUT',
    '1 samuel': '1SA',
    '2 samuel': '2SA',
    '1 kings': '1KI',
    '2 kings': '2KI',
    '1 chronicles': '1CH',
    '2 chronicles': '2CH',
    'ezra': 'EZR',
    'nehemiah': 'NEH',
    'esther (hebrew)': 'EST',
    'job': 'JOB',
    'psalms': 'PSA',
    'proverbs': 'PRO',
    'ecclesiastes': 'ECC',
    'song of songs': 'SNG',
    'isaiah': 'ISA',
    'jeremiah': 'JER',
    'lamentations': 'LAM',
    'ezekiel': 'EZK',
    'daniel (hebrew)': 'DAN',
    'hosea': 'HOS',
    'joel': 'JOL',
    'amos': 'AMO',
    'obadiah': 'OBA',
    'jonah': 'JON',
    'micah': 'MIC',
    'nahum': 'NAM',
    'habakkuk': 'HAB',
    'zephaniah': 'ZEP',
    'haggai': 'HAG',
    'zechariah': 'ZEC',
    'malachi': 'MAL',
    'matthew': 'MAT',
    'mark': 'MRK',
    'luke': 'LUK',
    'john': 'JHN',
    'acts': 'ACT',
    'romans': 'ROM',
    '1 corinthians': '1CO',
    '2 corinthians': '2CO',
    'galatians': 'GAL',
    'ephesians': 'EPH',
    'philippians': 'PHP',
    'colossians': 'COL',
    '1 thessalonians': '1TH',
    '2 thessalonians': '2TH',
    '1 timothy': '1TI',
    '2 timothy': '2TI',
    'titus': 'TIT',
    'philemon': 'PHM',
    'hebrews': 'HEB',
    'james': 'JAS',
    '1 peter': '1PE',
    '2 peter': '2PE',
    '1 john': '1JN',
    '2 john': '2JN',
    '3 john': '3JN',
    'jude': 'JUD',
    'revelation': 'REV',
    'tobit': 'TOB',
    'judith': 'JDT',
    'esther greek': 'ESG',
    'wisdom of solomon': 'WIS',
    'sirach': 'SIR',
    'baruch': 'BAR',
    'letter of jeremiah': 'LJE',
    'song of the 3 young men': 'S3Y',
    'susanna': 'SUS',
    'bel and the dragon': 'BEL',
    '1 maccabees': '1MA',
    '2 maccabees': '2MA',
    '3 maccabees': '3MA',
    '4 maccabees': '4MA',
    '1 esdras (greek)': '1ES',
    '2 esdras (latin)': '2ES',
    'prayer of manasseh': 'MAN',
    'psalm 151': 'PS2',
    'odae/odes': 'ODA',
    'psalms of solomon': 'PSS',
    'ezra apocalypse': 'EZA',
    '5 ezra': '5EZ',
    '6 ezra': '6EZ',
    'daniel greek': 'DAG',
    'psalms 152-155': 'PS3',
    '2 baruch (apocalypse)': '2BA',
    'letter of baruch': 'LBA',
    'jubilees': 'JUB',
    'enoch': 'ENO',
    '1 meqabyan/mekabis': '1MQ',
    '2 meqabyan/mekabis': '2MQ',
    '3 meqabyan/mekabis': '3MQ',
    'reproof': 'REP',
    '4 baruch': '4BA',
    'letter to the laodiceans': 'LAO',
}


def bibleBookNamesEnglish2UsfmMappings():
    """Get data from the first table in http://ubsicap.github.io/usfm/identification/books.html and return a mapping from english names to USFM names."""
    url = 'http://ubsicap.github.io/usfm/identification/books.html'
    tables = html2Json(get(url), convert_only_tables=True)

    assert len(tables) == 1
    table = tables[0]

    english_to_usfm_book_name_mappings = {i['English Name']: i['Identifier'] for i in table}
    return english_to_usfm_book_name_mappings


def bibleBookName2Usfm(book_name: str) -> typings.StringOrNone:
    """Convert the given book name (as either the english name or OSIS format) into USFM.

    Helpful sources: [http://ubsicap.github.io/usfm/identification/books.html]"""
    # TODO: handle book_name's which are in OSIS format

    usfm_book_name = BIBLE_BOOK_ENGLISH_NAMES_2_USFM_MAPPING.get(lowercase(book_name))
    return usfm_book_name
