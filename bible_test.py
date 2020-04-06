#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bible import bibleBookWordCountByChapter


def test_bibleBookWordCountByChapter_1():
    result = bibleBookWordCountByChapter('leviticus', 'atonement')
    assert isinstance(result, dict)
    assert result == {1: 1, 2: 0, 3: 0, 4: 4, 5: 5, 6: 1, 7: 1, 8: 1, 9: 2, 10: 1, 11: 0, 12: 2, 13: 0, 14: 7, 15: 2, 16: 15, 17: 2, 18: 0, 19: 1, 20: 0, 21: 0, 22: 0, 23: 3, 24: 0, 25: 1, 26: 0, 27: 0}

    result = bibleBookWordCountByChapter('leviticus')
    assert isinstance(result, dict)
    assert result == {1: 528, 2: 489, 3: 515, 4: 1160, 5: 724, 6: 892, 7: 1061, 8: 993, 9: 627, 10: 628, 11: 1115, 12: 262, 13: 1857, 14: 1717, 15: 920, 16: 1160, 17: 553, 18: 684, 19: 898, 20: 849, 21: 587, 22: 885, 23: 1223, 24: 554, 25: 1535, 26: 1246, 27: 960}
