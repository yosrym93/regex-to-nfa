# regex_nfa
Turn regex pattern into equivalent NFA using Thompson's algorithm.
Also renders NFA's graph.

# Usage
Call regex_nfa.py with regex pattern:
```
$ python3 ./regex_nfa.py 'A(B|A)*'
```

# Compilers Assignment 1 - Thompson's Algorithm
- Mahmoud Othman - BN 2 - SEC 19
- Yosry Mohammad - BN 2 - SEC 33

# Dependencies
- python3
- python3-pip
- graphviz
- py-graphviz

Install in debian/ubuntu:
```
$ sudo apt update && sudo apt install -y graphviz python3 python3-pip
$ sudo python3 -m pip install graphviz
```
