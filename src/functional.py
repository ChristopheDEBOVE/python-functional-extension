import dataclasses
from functools import partial
from typing import TypeVar, Generic, Callable

from pluggy import Result

T = TypeVar("T")


class Infix(object):
    def __init__(self, func):
        self.func = func

    def __or__(self, other):
        return self.func(other)

    def __ror__(self, other):
        return Infix(partial(self.func, other))

    def __call__(self, *args, **kwargs):
        return self.func()


@Infix
def map(result, fn: Callable[[T], T]) -> Result[T]:
    if result._error is not None:
        return result

    return Result.success(fn(result.value))


def as_success(result) -> Result[T]:
    return Result.success(result)


@Infix
def map_result(result, fn: Callable[[T], T]) -> Result[T]:
    return Result.success(fn(result))


@Infix
def success_bind(result, fn: Callable[[T], T]) -> Result[T]:
    return fn(result)


@Infix
def bind(result, fn: Callable[[T], T]) -> Result[T]:
    if result._error is not None:
        return result

    return fn(result.value)


@Infix
def if_failure(result, fn: Callable[[T], T]) -> Result[T]:
    if result._error is not None:
        return fn(result._error)

    return result


@Infix
def success_unsafe(result) -> Result[T]:
    if result.value is None:
        raise Exception("Trying to access nonexistent value")
    return result.value


@Infix
def tap(result, fn: Callable[[T], T]) -> Result[T]:
    fn(result)
    return result


@Infix
def error_unsafe(result) -> Result[T]:
    if result._error is None:
        raise Exception("Trying to access nonexistent error")
    return result._error


@Infix
def match(result, ma: tuple[Callable[[T], T], Callable[[str], T]]) -> T:
    if result._error is not None:
        return ma[1](result._error)

    return ma[0](result.value)


@Infix
def ensure(result, ma: tuple[Callable[[T], T], Exception]) -> T:
    if result._error is not None:
        return result

    if not ma[0](result.value):
        return Result.error(ma[1])

    return result


@dataclasses.dataclass
class Result(Generic[T]):
    _error: str | None = None
    value: T | None = None

    @classmethod
    def success(cls, value: T) -> "Result[T]":
        return cls(value=value)

    @classmethod
    def error(cls, error: Exception):
        return cls(_error=str(error))


def safe(func):
    def wrapper_safe(*args, **kwargs):
        try:
            return Result.success(func(*args, **kwargs))
        except Exception as e:
            return Result.error(e)

    return wrapper_safe