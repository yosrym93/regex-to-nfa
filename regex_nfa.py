#!/bin/env python3
"""\
Usage: regex_nfa.py <regex pattern>
    Turn regex pattern into equivalent NFA using Thompson's algorithm and renders NFA's graph.
    Outputs graph.png and graph.json \
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

    # print(tokens)
    # pretty_print_graph(graph)
    write_graph(graph)
    render(graph, pattern)


if __name__ == '__main__':
    main()
