import dataclasses
from functools import partial
from typing import TypeVar, Generic, Callable

T = TypeVar("T")


@dataclasses.dataclass
class Result(Generic[T]):
    _error: str | None = None
    _value: T | None = None

    @property
    def is_success(self) -> bool:
        return self._error is None

    @property
    def is_failure(self) -> bool:
        return self._error is not None

    @property
    def get_error_unsafe(self) -> str:
        if self.is_success:
            Exception("Trying to access nonexistent error")
        return self._error

    @property
    def get_value_unsafe(self) -> str:
        if self.is_failure:
            raise Exception("Trying to access nonexistent value")
        return self._value

    @classmethod
    def success(cls, value: T) -> "Result[T]":
        return cls(_value=value)

    @classmethod
    def error(cls, error: Exception):
        return cls(_error=str(error))

    def map(self, fn: Callable[[T], T]) -> "Result[T]":
        if self.is_failure:
            return self

        return Result.success(fn(self.get_value_unsafe))

    def tap(self, fn: Callable[[T], T]) -> "Result[T]":
        fn(self)
        return self

    @classmethod
    def combine(cls, name, email):
        pass


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
    return result.map(fn)


def as_success(result) -> Result[T]:
    return Result.success(result)


@Infix
def success_bind(result, fn: Callable[[T], T]) -> Result[T]:
    return fn(result)


@Infix
def bind(result, fn: Callable[[T], T]) -> Result[T]:
    if result.is_failure:
        return result

    return fn(result.get_value_unsafe)


@Infix
def if_failure(result, fn: Callable[[T], T]) -> Result[T]:
    if result.is_failure:
        return fn(result.get_error_unsafe)

    return result


@Infix
def success_unsafe(result) -> Result[T]:
    return result.get_value_unsafe


@Infix
def tap(result, fn: Callable[[T], T]) -> Result[T]:
    return result.tap(fn)


@Infix
def error_unsafe(result) -> Result[T]:
    return result.get_error_unsafe


@Infix
def match(result, ma: tuple[Callable[[T], T], Callable[[str], T]]) -> T:
    if result.is_failure:
        return ma[1](result.get_error_unsafe)

    return ma[0](result.get_value_unsafe)


@Infix
def ensure(result, ma: tuple[Callable[[T], T], Exception]) -> T:
    if result.is_failure:
        return result
    # check that part; seems buggy
    if not ma[0](result.get_value_unsafe):
        return Result.error(ma[1])

    return result


def safe(func):
    def wrapper_safe(*args, **kwargs):
        try:
            return Result.success(func(*args, **kwargs))
        except Exception as e:
            return Result.error(e)

    return wrapper_safe
