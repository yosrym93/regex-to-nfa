import sys
import json
from typing import Dict


def err(msg):
    print(msg, file=sys.stderr)
    exit(1)


def pretty_print_graph(graph: Dict):
    print(json.dumps(graph, indent=2, default=str))


def write_graph(graph: Dict):
    with open('graph.json', 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
