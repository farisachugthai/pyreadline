#!/usr/bin/env python
# -*- coding: utf-8 -*-
# yeah that got too frustrating too fast

import io
import tempfile
import tracemalloc
import unittest

from pyreadline.lineeditor.lineobj import ReadLineTextBuffer
from pyreadline.lineeditor.history import OrderedHistory

tracemalloc.start()


class TestOrderedHistory(unittest.TestCase):
    def setUp(self):
        self.buf = OrderedHistory(filename=tempfile.TemporaryFile())

    def tearDown(self):
        if self.buf is not None:
            self.buf.filename.close()

    def test_a_new_one(self):
        self.buf.clear()
        self.assertEqual(self.buf, [])
        self.assertLess(len(self.buf), 1)

    # def test_isinstance(self):
    #     self.assertIsInstance(self.buf, list)

    def test_index(self):
        # Does get_history_item say, index starts at 1?
        # FFS this passed
        with self.assertRaises(IndexError):
            self.buf.get_history_item(0)

    def test_adding_a_ReadLineTextBuffer_to_the_history(self):
        # like we jump through some acrobatic hoops for seemingly no reason
        self.buf.add_history(ReadLineTextBuffer("a simple str"))
        # NOPE! This actually doesn't pass as the str and the list are both
        # modified to our fucked ReadLineTextBuffer
        self.assertNotEqual(self.buf.history, ["a simple str"])
        self.assertNotEqual(self.buf.get_history_item(0), "a simple str")

    def test_getitem(self):
        self.buf.clear()
        self.buf = OrderedHistory(filename=tempfile.TemporaryFile())
        self.assertEqual(self.buf, [])
        self.buf.add_history("a simple str")
        self.assertEqual(self.buf[0], "a simple str")
        self.assertIsInstance(self.buf[0], str)

    def test_warmup_add(self):
        self.buf.clear()
        self.buf = OrderedHistory(filename=tempfile.TemporaryFile())
        self.assertEqual(self.buf, [])
        self.buf.history += ["Cross your fingers"]
        self.assertEqual(self.buf[0], "Cross your fingers")

    # def test_add(self):
    #     self.assertEqual(self.buf, [])
    #
    #     self.buf + ["Cross your fingers"]
    #     # print(vars(self.buf))
    #     self.assertEqual(self.buf[0], ["Cross your fingers"])

    # def test_iadd(self):
    #     self.assertEqual(self.buf, [])
    #     self.buf += "Cross your fingers"
    #     self.assertEqual(self.buf.history[0], "Cross your fingers")

    def test_other_shit(self):
        self.tuple_filename = OrderedHistory(filename=tempfile.mkstemp())
        # self.buf.
        print(dir(self.tuple_filename.filename))

    def test_len(self):
        self.buf2 = OrderedHistory()
        self.buf2.add_history("Anything")
        self.assertEqual(len(self.buf2), 1)
        del self.buf2.history[0]

    def test_inmemory_file(self):
        self.buf = OrderedHistory(filename=io.StringIO())


if __name__ == "__main__":
    unittest.main()
