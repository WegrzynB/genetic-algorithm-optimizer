# helpers.py
# Proste helpery narzędziowe.

from __future__ import annotations


def debug_print(verbose: bool, *args, **kwargs) -> None:
    # Wypisuje dane tylko wtedy, gdy tryb verbose jest aktywny.
    if verbose:
        print(*args, **kwargs)