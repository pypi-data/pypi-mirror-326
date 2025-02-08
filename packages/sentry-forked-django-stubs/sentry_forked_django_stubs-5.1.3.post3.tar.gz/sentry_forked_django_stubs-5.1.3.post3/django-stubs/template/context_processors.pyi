from collections.abc import Callable
from typing import TypeVar

from django.http.request import HttpRequest
from django.utils.functional import SimpleLazyObject

_R = TypeVar("_R", bound=HttpRequest)

def csrf(request: HttpRequest) -> dict[str, SimpleLazyObject]: ...
def debug(request: HttpRequest) -> dict[str, Callable | bool]: ...
def i18n(request: HttpRequest) -> dict[str, list[tuple[str, str]] | bool | str]: ...
def tz(request: HttpRequest) -> dict[str, str]: ...
def static(request: HttpRequest) -> dict[str, str]: ...
def media(request: HttpRequest) -> dict[str, str]: ...
def request(request: _R) -> dict[str, _R]: ...
