import abc
import collections

from types import TracebackType
from typing import Any, Callable, Dict, Tuple, TypeVar

__all__ = ['Thenable', 'ThenableProxy']

PromiseT = TypeVar('PromiseT', Callable, 'Thenable')


@collections.Callable.register
class Thenable(metaclass=abc.ABCMeta):  # pragma: no cover

    @abc.abstractmethod
    def __call__(self, *args, **kwargs) -> Any:
        ...

    @abc.abstractmethod
    def then(self, on_success: PromiseT,
             on_error: PromiseT = None) -> 'Thenable':
        ...

    @abc.abstractmethod
    def throw(self, exc: BaseException = None,
              tb: TracebackType = None,
              propagate: int = True) -> None:
        ...

    @abc.abstractmethod
    def throw1(self, exc: BaseException = None) -> None:
        ...

    @abc.abstractmethod
    def partial(self, *args, **kwargs) -> 'Thenable':
        ...

    @abc.abstractmethod
    def partial_inplace(self, *args, **kwargs) -> None:
        ...

    @abc.abstractmethod
    def clone(self, args: Tuple[Any, ...] = (), kwargs: Dict = {}) -> 'Thenable':
        ...

    @abc.abstractmethod
    def cancel(self) -> None:
        ...

    @property
    @abc.abstractmethod
    def cancelled(self) -> bool:
        ...

    @cancelled.setter
    def cancelled(self, cancelled: bool) -> None:
        ...

    @property
    @abc.abstractmethod
    def ready(self) -> bool:
        ...

    @ready.setter
    def ready(self, ready: bool) -> None:
        ...

    @property
    @abc.abstractmethod
    def failed(self) -> bool:
        ...

    @failed.setter
    def failed(self, failed: bool) -> None:
        ...

    @classmethod
    def __subclasshook__(cls: Any, C: Any) -> bool:
        if cls is Thenable:
            if any('then' in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented


class ThenableProxy(Thenable):

    def _set_promise_target(self, p: Thenable) -> None:
        self._p = p

    def then(self, on_success: PromiseT,
             on_error: PromiseT = None) -> Thenable:
        return self._p.then(on_success, on_error)

    def cancel(self) -> None:
        self._p.cancel()

    def throw1(self, exc: BaseException = None) -> None:
        self._p.throw1(exc)

    def throw(self, exc: BaseException = None,
              tb: TracebackType = None,
              propagate: int = True) -> None:
        self._p.throw(exc, tb=tb, propagate=propagate)

    @property
    def cancelled(self) -> bool:
        return self._p.cancelled

    @cancelled.setter
    def cancelled(self, cancelled: bool) -> None:
        self._p.cancelled = cancelled

    @property
    def ready(self) -> bool:
        return self._p.ready

    @ready.setter
    def ready(self, ready: bool) -> None:
        self._p.ready = None

    @property
    def failed(self) -> bool:
        return self._p.failed

    @failed.setter
    def failed(self, failed: bool) -> None:
        self._p.failed = None