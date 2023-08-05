import pathlib

from amino.typecheck import boot
from amino.maybe import Maybe, Just, Empty, may, flat_may, Nothing
from amino.either import Left, Right, Either
from amino.list import List
from amino.boolean import Boolean
from amino.anon import __, L, _
from amino.lazy_list import LazyList
from amino.map import Map
from amino.future import Future
from amino.func import curried, F, I
from amino.env_vars import env
from amino.task import Try, Task
from amino.logging import Logger, log
from amino.eff import Eff
from amino.eval import Eval
from amino.regex import Regex
from amino.options import integration_test, development

Path = pathlib.Path

boot()

__all__ = ('Maybe', 'Just', 'Empty', 'may', 'List', 'Map', '_', 'Future', 'Boolean', 'development', 'flat_may',
           'curried', '__', 'F', 'Left', 'Right', 'Either', 'env', 'Try', 'LazyList', 'Logger', 'log', 'I', 'L', 'Eff',
           'Task', 'Eval', 'Regex', 'Nothing', 'integration_test')
