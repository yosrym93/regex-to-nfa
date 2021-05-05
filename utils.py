import sys
import json
from typing import Dict


def err(msg):
    print(msg, file=sys.stderr)
    exit(1)


def pretty_print(graph: Dict):
    print(json.dumps(graph, indent=2, default=str))
