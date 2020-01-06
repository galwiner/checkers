import argparse

import checkersEngine as ce
import test_checkersEngine as tests

parser = argparse.ArgumentParser(description="Check a game of checkers and see who's the winner!")
parser.add_argument("-f", "--file", type=str, help="file name for the game.")
parser.add_argument("-t", "--tests", action="store_true", help="run the program test suite.")
parser.add_argument("-v", "--verbose", action="store_true", help="show debug messages")
parser.add_argument("-b", "--print_board", action="store_true", help="show the board")
parser.add_argument("-s", "--step", action="store_true", help="step through the game")

args = parser.parse_args()

if (args.file == None) & (not args.tests):
    parser.print_help()
if args.tests:
    tests.run_tests_extern()
if args.step:
    ce.PLAY_BY_PLAY = True
if args.print_board:
    ce.SHOW_BOARD = True
if args.verbose:
    ce.VERBOSE = True
ce.playGame(args.file)
# b = makeBoard()
# showBoard(b)
