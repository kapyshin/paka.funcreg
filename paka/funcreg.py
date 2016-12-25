import types
import functools
import collections


class _Registry(collections.defaultdict):

    def __init__(
            self, orig_key_checker, reg_key_maker, permitted_keys_factory,
            get_key_maker=None, default=None):
        super(_Registry, self).__init__(
            None if default is None else lambda: default)
        self._is_orig_key = orig_key_checker
        self._make_get_key = get_key_maker
        self._make_reg_key = reg_key_maker
        self._permitted_keys = permitted_keys_factory()

    def __getitem__(self, key):
        if self._make_get_key:
            key = self._make_get_key(key)
        return super(_Registry, self).__getitem__(key)

    def register(self, func_or_orig_key, orig_key=None):
        if (
                self._is_orig_key(func_or_orig_key, orig_key) or
                func_or_orig_key in self._permitted_keys):
            def inner(func):
                self[self._make_reg_key(func, func_or_orig_key)] = func
                return func
            return inner
        else:
            key = self._make_reg_key(func_or_orig_key, orig_key)
            self[key] = func_or_orig_key
            return func_or_orig_key

    def add_key(self, obj):
        self._permitted_keys.add(obj)
        return obj


_make_registry_factory = functools.partial(functools.partial, _Registry)


def _check_obj_or_type_key(maybe_orig_key, orig_key):
    return (
        orig_key is None and
        not isinstance(maybe_orig_key, types.FunctionType))


NameRegistry = _make_registry_factory(
    orig_key_checker=lambda maybe_orig_key, _: not callable(maybe_orig_key),
    reg_key_maker=lambda func, name: name or func.__name__,
    permitted_keys_factory=set)

ObjectRegistry = _make_registry_factory(
    orig_key_checker=_check_obj_or_type_key,
    reg_key_maker=lambda func, obj: obj or func,
    permitted_keys_factory=set)

TypeRegistry = _make_registry_factory(
    orig_key_checker=_check_obj_or_type_key,
    reg_key_maker=lambda func, type_: type_ or type(func),
    get_key_maker=type,
    permitted_keys_factory=set)
