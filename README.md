# checkers
home test for Sight DX

# Usage

checkersCLI.py is a command line interface to run the tests. 

You can run `python checkersCLI.py` to get usage instructions. 

`python checkersCLI.py - t` runs the test files attached with the original zip file 

`python checkersCLI.py -f "filename"` runs the game for a specific file

`python checkersCLI.py -b -f "filename"` runs the game and shows a board on each move

`python checkersCLI.py -s -b -f "filename"` runs the game and shows a board on each move, waiting for user click for next step

# Structure 

checkersEngine.py implements the function for the checkers game. 

I've tried to implement it in a functional style, meaning mostly (in this case) that nothing is modified and when moves are performed a copy of the board is returned. 

test_checkersEngine.py is a unittest based simple test suite which tests the required input files. 

checkersCLI.py uses argparse to build a basic CLI to run the game

# time spent

~~About 5 hours all and all~~ About 6.5 hours all and all after corrections.

I've not done any python in a while so I was a bit rusty. Also, it was fun so I played so more.



