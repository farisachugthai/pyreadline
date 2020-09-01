# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Jörgen Stenarson. <>
from __future__ import print_function, unicode_literals, absolute_import

import sys
import unittest

import pyreadline
from pyreadline.lineeditor.lineobj import ReadLineTextBuffer
from pyreadline.lineeditor.history import LineHistory
from pyreadline.lineeditor import history

sys.path.append("../..")

# ----------------------------------------------------------------------
# Globals
# ----------------------------------------------------------------------

# pyreadline.logger.sock_silent = False

global RL
RL = ReadLineTextBuffer
l = ReadLineTextBuffer("First Second Third")


class Test_prev_next_history(unittest.TestCase):
    t = "test text"

    def setUp(self):
        self.q = LineHistory()
        q = self.q
        for x in ["aaaa", "aaba", "aaca", "akca", "bbb", "ako"]:
            q.add_history(RL(x))

    def test_previous_history(self):
        hist = self.q
        assert hist.history_cursor == 6
        l = RL("")
        hist.previous_history(l)
        assert l.get_line_text() == "ako"
        hist.previous_history(l)
        assert l.get_line_text() == "bbb"
        hist.previous_history(l)
        assert l.get_line_text() == "akca"
        hist.previous_history(l)
        assert l.get_line_text() == "aaca"
        hist.previous_history(l)
        assert l.get_line_text() == "aaba"
        hist.previous_history(l)
        assert l.get_line_text() == "aaaa"
        hist.previous_history(l)
        assert l.get_line_text() == "aaaa"

    def test_next_history(self):
        hist = self.q
        hist.beginning_of_history()
        assert hist.history_cursor == 0
        l = RL("")
        hist.next_history(l)
        assert l.get_line_text() == "aaba"
        hist.next_history(l)
        assert l.get_line_text() == "aaca"
        hist.next_history(l)
        assert l.get_line_text() == "akca"
        hist.next_history(l)
        assert l.get_line_text() == "bbb"
        hist.next_history(l)
        assert l.get_line_text() == "ako"
        hist.next_history(l)
        assert l.get_line_text() == "ako"


class TestPrevNextHistory(unittest.TestCase):
    t = "test text"

    def setUp(self):
        self.q = q = LineHistory()
        for x in ["aaaa", "aaba", "aaca", "akca", "bbb", "ako"]:
            q.add_history(RL(x))

    def test_history_search_backward(self):
        #  TODO. the for loops are ripe for self.subtests
        q = LineHistory()
        for x in ["aaaa", "aaba", "aaca", "    aacax", "akca", "bbb", "ako"]:
            q.add_history(RL(x))
        a = RL("aa", point=2)
        for x in ["aaca", "aaba", "aaaa", "aaaa"]:
            res = q.history_search_backward(a)
            assert res.get_line_text() == x

    def test_history_search_forward(self):
        q = LineHistory()
        for x in ["aaaa", "aaba", "aaca", "    aacax", "akca", "bbb", "ako"]:
            q.add_history(RL(x))
        q.beginning_of_history()
        a = RL("aa", point=2)
        for x in ["aaba", "aaca", "aaca"]:
            res = q.history_search_forward(a)
            assert res.get_line_text() == x


class Test_history_search_incr_fwd_backwd(unittest.TestCase):
    # TODO: self.subtests omg

    def setUp(self):
        self.q = q = LineHistory()
        for x in ["aaaa", "aaba", "aaca", "akca", "bbb", "ako"]:
            q.add_history(RL(x))

    def test_backward_1(self):
        self.assertEqual(self.q.reverse_search_history("b"), "bbb")
        self.assertEqual(self.q.reverse_search_history("b"), "aaba")
        self.assertEqual(self.q.reverse_search_history("bb"), "aaba")

    def test_backward_2(self):
        self.assertEqual(self.q.reverse_search_history("a"), "ako")
        self.assertEqual(self.q.reverse_search_history("aa"), "aaca")
        self.assertEqual(self.q.reverse_search_history("a"), "aaca")
        self.assertEqual(self.q.reverse_search_history("ab"), "aaba")

    def test_forward_1(self):
        self.assertEqual(self.q.forward_search_history("a"), "ako")

    def test_forward_2(self):
        self.q.history_cursor = 0
        self.assertEqual(self.q.forward_search_history("a"), "aaaa")
        self.assertEqual(self.q.forward_search_history("a"), "aaba")
        self.assertEqual(self.q.forward_search_history("ak"), "akca")
        self.assertEqual(self.q.forward_search_history("akl"), "akca")
        self.assertEqual(self.q.forward_search_history("ak"), "akca")
        self.assertEqual(self.q.forward_search_history("ako"), "ako")


class Test_empty_history_search_incr_fwd_backwd(unittest.TestCase):
    def setUp(self):
        self.q = q = LineHistory()

    def test_backward_1(self):
        q = self.q
        self.assertEqual(q.reverse_search_history("b"), "")

    def test_forward_1(self):
        q = self.q
        self.assertEqual(q.forward_search_history("a"), "")


class TestLineHistoryDunderMethods(unittest.TestCase):
    def setUp(self):
        self.buf = LineHistory()

    def test_index(self):
        # Does get_history_item say, index starts at 1?
        # FFS this passed
        with self.assertRaises(IndexError):
            self.buf.get_history_item(0)

    def test_adding_a_ReadLineTextBuffer_to_the_history(self):
        # like we jump through some acrobatic hoops for seemingly no reason
        self.buf.add_history("a simple str")
        # NOPE! This actually doesn't pass as the str and the list are both
        # modified to our fucked ReadLineTextBuffer
        self.assertEqual(self.buf.history, ["a simple str"])
        self.assertEqual(self.buf.get_history_item(0), "a simple str")

    def test_getitem(self):
        self.buf = LineHistory()
        self.buf.add_history("a simple str")
        self.assertEqual(self.buf[0], "a simple str")

    def test_add(self):
        self.adding_buffer = LineHistory()
        self.adding_buffer + "Cross your fingers"
        self.assertEqual(self.buf[0], "Cross your fingers")

    def test_len(self):
        self.buf2 = LineHistory()
        self.buf2.add_history("Anything")
        self.assertEqual(len(self.buf2), 1)
        del self.buf2.history[0]

    def test_a_new_one(self):
        self.new_buffer = LineHistory()
        self.assertLess(len(self.new_buffer), 1)


if __name__ == "__main__":
    unittest.main()
