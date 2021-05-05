#!/bin/env python3
"""\
Usage: regex_nfa.py pattern
Turn regex pattern into equivalent NFA using Thompson's algorithm.
Also renders NFA's graph.

Compilers Assignment 1 - Thompson's Algorithm
    Mahmoud Othman - BN 2 - SEC 19
    Yosry Mohammad - BN 2 - SEC 33

Dependencies
    python3, python3-pip, graphviz, py-graphviz
    $ sudo apt update && sudo apt install -y graphviz python3 python3-pip
    $ sudo python3 -m pip install graphviz \
"""
from utils import *
from token_parser import regex_to_tokens
from nfa_generator import tokens_to_nfa
from graph_generator import render


def main():
    if len(sys.argv) != 2:
        err(__doc__)

    if sys.argv[1] in ('-h', '--help'):
        print(__doc__)
        exit(0)

    pattern = sys.argv[1]
    tokens = regex_to_tokens(pattern)
    graph = tokens_to_nfa(tokens)

    pretty_print(graph)
    render(graph, pattern)


if __name__ == '__main__':
    main()
