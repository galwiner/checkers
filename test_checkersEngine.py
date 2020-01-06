from unittest import TestCase
import unittest
from checkersEngine import *


class Test(TestCase):
    def test_white_wins(self):
        res = playGame('white.txt')
        self.assertEqual(res, "white wins")

    def test_black_wins(self):
        res = playGame('black.txt')
        self.assertEqual(res, "black wins")

    def test_illegal_move(self):
        res = playGame('illegal_move.txt')
        self.assertEqual(res, "Line 15  illegal move [1 0 0 5]")

    def test_incomplete_game(self):
        res = playGame('incomplete.txt')
        self.assertEqual(res, "incomplete game")


def run_tests_extern():
    runner = unittest.TextTestRunner()
    result = runner.run(unittest.makeSuite(Test))