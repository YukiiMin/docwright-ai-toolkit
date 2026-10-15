"""
CLI entrypoint when invoked via `python -m doctools`.
"""
import sys
from doctools.cli import main

if __name__ == "__main__":
    sys.exit(main())
