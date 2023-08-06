
import unittest

from cheddar.util.itertools import chunk, chunk_truncate, chunk_fill
from cheddar.util.itertools import consecutive


@unittest.skip("")
class TestItertools(unittest.TestCase):

    def setUp(self):
        pass

    def test_chunk(self):
        f = lambda a, b: tuple("".join(seq) for seq in chunk(a, b))
        self.assertEqual(f("ABCDEFGHI", 3), ("ABC", "DEF", "GHI"))
        self.assertEqual(f("ABCDEFGHIJ", 3), ("ABC", "DEF", "GHI", "J"))
        self.assertEqual(f("", 3), ())
        self.assertEqual(f("ABCDEFGHIJ", 0), ())
        self.assertEqual(f("ABCDEFGHIJ", 10), ("ABCDEFGHIJ",))
        self.assertEqual(f("ABCDEFGHIJ", 11), ("ABCDEFGHIJ",))

    def test_chunk_truncate(self):
        f = lambda a, b: tuple("".join(seq) for seq in chunk_truncate(a, b))
        self.assertEqual(f("ABCDEFGHI", 3), ("ABC", "DEF", "GHI"))
        self.assertEqual(f("ABCDEFGHIJ", 3), ("ABC", "DEF", "GHI"))
        self.assertEqual(f("", 3), ())
        self.assertEqual(f("ABCDEFGHIJ", 0), ())
        self.assertEqual(f("ABCDEFGHIJ", 10), ("ABCDEFGHIJ",))
        self.assertEqual(f("ABCDEFGHIJ", 11), ())

    def test_chunk_fill(self):
        f = lambda a, b, x: tuple("".join(seq) for seq in chunk_fill(a, b, x))
        self.assertEqual(f("ABCDEFGHI", 3, 'x'), ("ABC", "DEF", "GHI"))
        self.assertEqual(f("ABCDEFGHIJ", 3, 'x'), ("ABC", "DEF", "GHI", "Jxx"))
        self.assertEqual(f("", 3, 'x'), ())
        self.assertEqual(f("ABCDEFGHIJ", 0, 'x'), ())
        self.assertEqual(f("ABCDEFGHIJ", 10, 'x'), ("ABCDEFGHIJ",))
        self.assertEqual(f("ABCDEFGHIJ", 11, 'x'), ("ABCDEFGHIJx",))

    def test_consecutive(self):
        f = lambda a, b: tuple("".join(seq) for seq in consecutive(a, b))
        self.assertEqual(f("ABCDEF", 3), ("ABC", "BCD", "CDE", "DEF"))
        self.assertEqual(f("", 3), ())
        self.assertEqual(f("ABCDEF", 0), ())
        self.assertEqual(f("ABCDEF", 6), ("ABCDEF",))
        self.assertEqual(f("ABCDEF", 7), ())
