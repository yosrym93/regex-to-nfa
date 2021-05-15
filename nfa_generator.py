from typing import List

from constants import *
from utils import *
from token_parser import Token, CharToken, AndToken, OrToken, ZeroOrMoreToken, TokenType


class State:
    _next_state_id: int = 1
    _states: List = []

    @classmethod
    def new(cls, is_terminating=False):
        s = State(cls._next_state_id, is_terminating)
        cls._states.append(s)
        cls._next_state_id += 1
        return s

    @classmethod
    def get_nfa_dict(cls, initial_state_id):
        nfa = {"startingState": f"S{initial_state_id}"}
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
    s1 = State.new()
    s4 = State.new()
    for next_state_id in next_states_ids:
        s4.add_transition(EPSILON, next_state_id)
    s2_id = generate_token_states(token.a, [s4.id])
    s3_id = generate_token_states(token.b, [s4.id])
    s1.add_transition(EPSILON, s2_id)
    s1.add_transition(EPSILON, s3_id)
    return s1.id


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
    final_state = State.new(is_terminating=True)
    initial_state_id = generate_token_states(tokens, [final_state.id])
    return State.get_nfa_dict(initial_state_id)
