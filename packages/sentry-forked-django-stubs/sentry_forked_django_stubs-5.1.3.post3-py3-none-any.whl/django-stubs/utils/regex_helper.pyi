from collections.abc import Iterator, Mapping
from re import Pattern
from typing import TypeVar

ESCAPE_MAPPINGS: Mapping[str, str | None]

class Choice(list): ...
class Group(list): ...
class NonCapture(list): ...

def normalize(pattern: str) -> list[tuple[str, list[str]]]: ...
def next_char(input_iter: Iterator[str]) -> Iterator[tuple[str, bool]]: ...
def walk_to_end(ch: str, input_iter: Iterator[tuple[str, bool]]) -> None: ...
def get_quantifier(ch: str, input_iter: Iterator[tuple[str, bool]]) -> tuple[int, str | None]: ...
def contains(source: Group | NonCapture | str, inst: type[Group]) -> bool: ...
def flatten_result(
    source: list[Choice | Group | str] | Group | NonCapture | None,
) -> tuple[list[str], list[list[str]]]: ...

# Returns SimpleLazyObject, but we can safely ignore it
_P = TypeVar("_P", str, bytes)

def _lazy_re_compile(regex: _P | Pattern[_P], flags: int = 0) -> Pattern[_P]: ...
