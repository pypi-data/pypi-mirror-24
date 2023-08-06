import inspect
from functools import wraps
from collections import defaultdict
from contextlib import contextmanager

from .servant import Servant
from .utils import Sentinel, annotate, ExitQueue


def member(directive):
    return annotate(member=directive)


Undefined = Sentinel("Undefined", "muster", "no value")


def dispatch(method):
    @wraps(method)
    def wrapper(self, obj, **kwargs):
        action = method.__name__
        with self.distpatcher(obj, action, kwargs):
            return method(self, obj, **kwargs)
    return wrapper


class Member(Servant):

    directives = ("when", "then")

    def __init__(self, parent=None, **data):
        self.data = {}
        self.callbacks = defaultdict(list)
        super(Member, self).__init__(parent)
        self.data.update(data)

    def inherit(self, parent):
        super(Member, self).inherit(parent)
        self.data.update(parent.data)
        for action, methods in parent.callbacks.items():
            self.callbacks[action].extend(methods)
        
    def when(self, owner, action, name):
        store = self.callbacks[action]
        if name not in store:
            store.append(name)
        method = getattr(owner, name)
        self._wrap_context_method(owner, name)

    def then(self, owner, after, before):
        method = getattr(owner, after)
        selector, command, action = self.resolve_directive(method)
        if not self.is_my_directive(owner, selector, command):
            raise TypeError("%r is not my directive" % after)
        index = self.callbacks[action].index(after)
        self.callbacks[action].insert(index, before)
        self._wrap_context_method(owner, before)

    @staticmethod
    def _wrap_context_method(cls, name):
        method = getattr(cls, name)
        if inspect.isgeneratorfunction(method):
            setattr(cls, name, contextmanager(method))

    @dispatch
    def set(self, obj, value):
        setattr(obj, self.private, value)

    @dispatch
    def delete(self, obj):
        try:
            delattr(self, self.private)
        except AttributeError:
            raise AttributeError(self.public)

    @dispatch
    def default(self, obj, value=Undefined):
        if value is Undefined:
            raise AttributeError(self.public)
        else:
            setattr(self, self.private, value)
            return value

    def get(self, obj):
        try:
            return getattr(obj, self.private)
        except AttributeError:
            return self.default(obj)

    @contextmanager
    def distpatcher(self, obj, action, kwargs):
        with ExitQueue() as queue:
            for cb in self.callbacks[action]:
                context = getattr(obj, cb)(self, **kwargs)
                out = queue.enter_context(context)
                kwargs.update(out or {})
            yield


    def __set__(self, obj, val):
        self.set(obj, value=val)

    def __get__(self, obj, cls):
        if obj is not None:
            return self.get(obj)
        else:
            return self

    def __delete__(self, obj):
        self.delete(obj)
