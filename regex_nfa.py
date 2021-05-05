#!/bin/env python3
"""
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
import sys
from typing import Dict, Generator, NamedTuple, Tuple, List, Union
import json
from graphviz import Digraph

OR_META = ('+', '|')
ALL_META = OR_META + ('*',)

# best rendering by graphviz
EPSILON = '<&epsilon;>'


def err(msg):
    print(msg, file=sys.stderr)
    exit(1)


class Token:
    pass


class CharToken(NamedTuple):
    # one character
    value: str


class AndToken(NamedTuple):
    a: Token
    b: Token


class OrToken(NamedTuple):
    a: Token
    b: Token


class ZeroOrMoreToken(NamedTuple):
    # token repeated 0 or more times
    a: Token


TokenType = Union[Token, CharToken, AndToken, OrToken, ZeroOrMoreToken]

def _invalid_strs():
    for a in ALL_META:
        for b in ALL_META:
            yield f'{a}{b}'


def _get_chartoken(pattern: str) -> TokenType:
    assert len(pattern) >= 1

    ct = CharToken(pattern[0])

    # peek to see *
    if len(pattern) >= 2 and pattern[1] == '*':
        return ZeroOrMoreToken(ct)
    return ct


def regex_to_tokens(pattern: str) -> TokenType:
    """
    regex_to_tokens takes regex pattern and returns token tree
    handles errors in the pattern
    """
    if len(pattern) == 0:
        return CharToken('')

    # handle all possible errors
    if pattern[0] in ALL_META:
        err('invalid token at index 0')
    if pattern[-1] in OR_META:
        err(f'invalid token at index {len(pattern)}')
    for s in _invalid_strs():
        i = pattern.find(s)
        if i != -1:
            err(f'invalid token at index {i}')

    t = CharToken(pattern[0])
    i = 1
    while i < len(pattern):
        if pattern[i] not in ALL_META:
            t = AndToken(t, _get_chartoken(pattern[i:]))
        elif pattern[i] in OR_META:
            # safe to check next character
            # we know there is no + or | at the end
            i += 1
            t = OrToken(t, _get_chartoken(pattern[i:]))
        else:  # * is handled
            pass

        i += 1

    return t


class State:
    _next_state_id: int = 0
    _states: List = []

    @classmethod
    def new(cls, is_terminating=False):
        s = State(cls._next_state_id, is_terminating)
        cls._states.append(s)
        cls._next_state_id += 1
        return s

    @classmethod
    def get_nfa_dict(cls):
        nfa = {"startingState": "S0"}
        for state in cls._states:
            state_name = f'S{state.id}'
            nfa[state_name] = {"isTerminatingState": state.is_terminating}
            for state_input, next_states_ids in state.output_transitions.items():
                nfa[state_name][state_input] = []
                for next_state_id in next_states_ids:
                    next_state_name = f'S{next_state_id}'
                    nfa[state_name][state_input].append(next_state_name)
        return nfa

    def __init__(self, state_id, is_terminating=False):
        self.id: int = state_id
        self.output_transitions: Dict[str, List[int]] = {}
        self.is_terminating: bool = is_terminating

    def add_transition(self, state_input, next_state_id):
        if state_input in self.output_transitions:
            self.output_transitions[state_input].append(next_state_id)
        else:
            self.output_transitions[state_input] = [next_state_id]


def generate_char_token_states(token: CharToken, next_states_ids: List[int]) -> int:
    s1 = State.new()
    s2 = State.new()
    s1.add_transition(token.value, s2.id)
    for next_state_id in next_states_ids:
        s2.add_transition(EPSILON, next_state_id)
    return s1.id


def generate_and_token_states(token: AndToken, next_states_ids: List[int]) -> int:
    s2_id = generate_token_states(token.b, next_states_ids)
    s1_id = generate_token_states(token.a, [s2_id])
    return s1_id


def generate_or_token_states(token: OrToken, next_states_ids: List[int]) -> int:
    s = State.new()
    s1_id = generate_token_states(token.a, next_states_ids)
    s2_id = generate_token_states(token.b, next_states_ids)
    s.add_transition(EPSILON, s1_id)
    s.add_transition(EPSILON, s2_id)
    return s.id


def generate_zero_or_more_token_states(token: ZeroOrMoreToken, next_states_ids: List[int]) -> int:
    s1 = State.new()
    s3 = State.new()
    for next_state_id in next_states_ids:
        s3.add_transition(EPSILON, next_state_id)
    s2_id = generate_token_states(token.a, [s1.id, s3.id])
    s1.add_transition(EPSILON, s2_id)
    s1.add_transition(EPSILON, s3.id)
    return s1.id


def generate_token_states(token: TokenType, next_states_ids: List[int]) -> int:
    if isinstance(token, CharToken):
        return generate_char_token_states(token, next_states_ids)
    elif isinstance(token, AndToken):
        return generate_and_token_states(token, next_states_ids)
    elif isinstance(token, OrToken):
        return generate_or_token_states(token, next_states_ids)
    elif isinstance(token, ZeroOrMoreToken):
        return generate_zero_or_more_token_states(token, next_states_ids)
    else:
        err("Unknown token type")


def tokens_to_nfa(tokens: Token) -> Dict:
    """
    tokens_to_nfa turns the tokens after parsing to NFA graph
    output is a dictionary following the output specs in the requirements file
    """
    print(tokens)
    initial_state = State.new()
    final_state = State.new(is_terminating=True)
    next_state_id = generate_token_states(tokens, [final_state.id])
    initial_state.add_transition(EPSILON, next_state_id)
    return State.get_nfa_dict()


def _gen_states(graph: Dict) -> Generator[Tuple[str, Dict], None, None]:
    for k, v in graph.items():
        if k == 'startingState':
            continue
        yield k, v


class _Edge(NamedTuple):
    trigger: str
    to: List[str]


def _gen_state_edges(state: Dict) -> Generator[_Edge, None, None]:
    for k, v in state.items():
        if k == 'isTerminatingState':
            continue
        for next_state in v:
            yield _Edge(trigger=k, to=next_state)


def render(graph: Dict, pattern: str):
    """ render takes the final graph output and renders it using graphviz """
    dot = Digraph(comment=f"NFA Graph for regex='{pattern}'")

    for state, v in _gen_states(graph):
        # node
        shape = 'doublecircle' if v['isTerminatingState'] else 'circle'
        dot.node(state, shape=shape)

        # edges
        for edge in _gen_state_edges(v):
            dot.edge(state, edge.to, label=edge.trigger)

    # empty node for start edge
    dot.node('', shape='point', style='invis')
    dot.edge('', graph['startingState'], label=EPSILON)

    dot.render('./graph', view=True, format='png', cleanup=True)


def pretty_print(graph: Dict):
    print(json.dumps(graph, indent=2, default=str))


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
