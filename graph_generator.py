from typing import Dict, Generator, NamedTuple, Tuple, List
from graphviz import Digraph

from constants import *


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
    dot = Digraph(comment=f"NFA Graph for regex='{pattern}'",
                  graph_attr={'rankdir': 'LR'})

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
