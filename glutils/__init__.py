import sys

from .enricher import Enricher

def log(*values):
    print(*values, file=sys.stderr)
