import abc
import time
import traceback
import inspect
from typing import Callable, TypeVar, Generic, Any, Coroutine

from fn.recur import tco

from amino import Either, Right, Left, Maybe, List, Empty, __, Just, env, _, Lists, L
from amino.tc.base import Implicits, ImplicitsMeta
from amino.logging import log
from amino.util.fun import lambda_str, format_funcall
from amino.util.exception import format_exception, sanitize_tb

A = TypeVar('A')
B = TypeVar('B')


class TaskException(Exception):
    remove_pkgs = List('amino', 'fn')

    def __init__(self, f, stack, cause) -> None:
        self.f = f
        self.stack = List.wrap(stack)
        self.cause = cause

    @property
    def location(self):
        files = List('task', 'anon', 'instances/task', 'tc/base')
        def filt(entry, name):
            return entry.filename.endswith('/amino/{}.py'.format(name))
        stack = self.stack.filter_not(lambda a: files.exists(L(filt)(a, _)))
        pred = (lambda a: not TaskException.remove_pkgs
                .exists(lambda b: '/{}/'.format(b) in a.filename))
        return stack.find(pred)

    @property
    def format_stack(self) -> List[str]:
        rev = self.stack.reversed
        def remove_recursion(i):
            pre = rev[:i + 1]
            post = rev[i:].drop_while(__.filename.endswith('/amino/task.py'))
            return pre + post
        def remove_internal():
            start = rev.index_where(_.function == 'unsafe_perform_sync')
            return start / remove_recursion | rev
        frames = (self.location.to_list if Task.stack_only_location else remove_internal())
        data = frames / (lambda a: a[1:-2] + tuple(a[-2]))
        return sanitize_tb(Lists.wrap(traceback.format_list(list(data))))

    @property
    def lines(self) -> List[str]:
        cause = format_exception(self.cause)
        suf1 = '' if self.stack.empty else ' at:'
        tb1 = (List() if self.stack.empty else self.format_stack)
        return tb1.cons(f'Task exception{suf1}').cat('Cause:') + cause + List(
            '',
            'Callback:',
            f'  {self.f}'
        )

    def __str__(self):
        return self.lines.join_lines


class TaskMeta(ImplicitsMeta):

    @property
    def zero(self):
        return Task.now(None)


class Task(Generic[A], Implicits, implicits=True, metaclass=TaskMeta):
    debug = 'AMINO_TASK_DEBUG' in env
    stack_only_location = True

    def __init__(self) -> None:
        self.stack = inspect.stack() if Task.debug else []

    @staticmethod
    def delay(f: Callable[..., A], *a, **kw):
        try:
            s = format_funcall(f, a, kw)
        except Exception as e:
            s = str(f)
            log.error(e)
        return Suspend(L(f)(*a, **kw) >> Now, s)

    @staticmethod
    def suspend(f: Callable[..., 'Task[A]'], *a, **kw):
        try:
            s = format_funcall(f, a, kw)
        except Exception as e:
            s = str(f)
            log.error(e)
        return Suspend(L(f)(*a, **kw), s)

    @staticmethod
    def call(f: Callable[..., A], *a, **kw):
        return Task.delay(f, *a, **kw)

    @staticmethod
    def now(a: A) -> 'Task[A]':
        return Now(a)

    @staticmethod
    def pure(a: A) -> 'IO[A]':
        return Pure(a)

    @staticmethod
    def just(a: A) -> 'Task[Maybe[A]]':
        return Task.now(Just(a))

    @staticmethod
    def failed(err: str) -> 'Task[A]':
        def fail():
            raise Exception(err)
        return Task.suspend(fail)

    @staticmethod
    def from_either(a: Either[Any, A]) -> 'Task[A]':
        return a.cata(Task.failed, Task.now)

    @staticmethod
    def from_maybe(a: Maybe[A], error: str) -> 'Task[A]':
        return a / Task.now | Task.failed(error)

    def run(self):
        @tco
        def run(t):
            if isinstance(t, Now):
                return True, (t.value,)
            elif isinstance(t, Task):
                return True, (t.step(),)
            else:
                return False, t
        return run(self)

    @property
    def _name(self):
        return self.__class__.__name__

    def flat_map(self, f: Callable[[A], 'Task[B]'], ts=Empty(), fs=Empty()
                 ) -> 'Task[B]':
        ts = ts | (lambda: self.string)
        fs = fs | (lambda: 'flat_map({})'.format(lambda_str(f)))
        return self._flat_map(f, ts, fs)

    @abc.abstractmethod
    def _flat_map(self, f: Callable[[A], 'Task[B]'], ts, fs) -> 'Task[B]':
        ...

    def step(self):
        try:
            return self._step_timed() if Task.debug else self._step()
        except TaskException as e:
            raise e
        except Exception as e:
            raise TaskException(self.string, self.stack, e)

    @abc.abstractmethod
    def _step(self):
        ...

    def _step_timed(self):
        start = time.time()
        v = self._step()
        dur = time.time() - start
        if dur > 0.1:
            log.ddebug(lambda: 'task {} took {:.4f}s'.format(self.string, dur))
        return v

    def __repr__(self):
        return 'Task({})'.format(self.string)

    @property
    def attempt(self) -> Either[Exception, A]:
        try:
            return Right(self.run())
        except TaskException as e:
            return Left(e)

    def unsafe_perform_sync(self):
        return self.attempt

    @property
    def fatal(self) -> A:
        return self.attempt.get_or_raise

    def and_then(self, nxt: 'Task[B]'):
        fs = 'and_then({})'.format(nxt.string)
        return self.flat_map(lambda a: nxt, fs=Just(fs))

    __add__ = and_then

    def join_maybe(self, err):
        return self.flat_map(lambda a: Task.from_maybe(a, err))

    @property
    def join_either(self):
        return self.flat_map(Task.from_either)

    def with_string(self, s):
        self.string = s
        return self

    def with_stack(self, s):
        self.stack = s
        return self

    def recover(self, f: Callable[[TaskException], B]) -> 'Task[B]':
        return Task.delay(self.unsafe_perform_sync).map(__.value_or(f))

    @property
    def coro(self) -> Coroutine:
        async def coro() -> Either[TaskException, A]:
            return self.attempt
        return coro()


class Suspend(Generic[A], Task[A]):

    def __init__(self, thunk: Callable, string) -> None:
        super().__init__()
        self.thunk = thunk
        self.string = string

    def _step(self):
        return self.thunk().with_stack(self.stack)

    def __str__(self):
        return '{}({})'.format(self._name, self.string)

    def _flat_map(self, f: Callable[[A], 'Task[B]'], ts, fs) -> 'Task[B]':
        return BindSuspend(self.thunk, f, ts, fs)


class BindSuspend(Generic[A], Task[A]):

    def __init__(self, thunk, f: Callable, ts, fs) -> None:
        super().__init__()
        self.thunk = thunk
        self.f = f
        self.ts = ts
        self.fs = fs

    def _step(self):
        return (
            self.thunk()
            .flat_map(self.f, fs=Just(self.fs))
            .with_stack(self.stack)
        )

    def __str__(self):
        return '{}({})'.format(self._name, self.string)

    def _flat_map(self, f: Callable[[A], 'Task[B]'], ts, fs) -> 'Task[B]':
        bs = L(BindSuspend)(self.thunk, lambda a: self.f(a).flat_map(f, Just(ts), Just(fs)), ts, fs)
        return Suspend(bs, '{}.{}'.format(ts, fs))

    @property
    def string(self):
        return '{}.{}'.format(self.ts, self.fs)


class Now(Generic[A], Task[A]):

    def __init__(self, value) -> None:
        super().__init__()
        self.value = value

    def _step(self):
        return self

    def __str__(self):
        return '{}({})'.format(self._name, self.value)

    def _flat_map(self, f: Callable[[A], 'Task[B]'], ts, fs) -> 'Task[B]':
        return Suspend(L(f)(self.value), '{}.{}'.format(ts, fs))

    @property
    def ts(self):
        return 'Task'

    @property
    def fs(self):
        return 'now({})'.format(self.value)

    @property
    def string(self) -> str:
        return str(self)

Pure = Now


def Try(f: Callable[..., A], *a, **kw) -> Either[Exception, A]:
    try:
        return Right(f(*a, **kw))
    except Exception as e:
        return Left(e)


def task(fun):
    def dec(*a, **kw):
        return Task.delay(fun, *a, **kw)
    return dec

IO = Task

__all__ = ('Task', 'Try', 'task', 'IO')
