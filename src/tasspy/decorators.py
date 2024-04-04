from functools import wraps
from typing import Callable, NoReturn, Optional
from .validators import KwargsValidator, KwargValueValidator, _requests_kwargs


def rename_class_param(fn_param: str, _param: str = "class") -> Callable:
    """Decorator that 'renames' a function parameter if it clashes with a reserved word in Python.
    For example, replaces 'studclass' method parameter with 'class' parameter in kwargs."""

    def wrapper(fn: Callable) -> Callable:
        @wraps(fn)
        def wrap_actions(self, *args, **kwargs) -> Optional[dict]:
            if kwargs and (value := kwargs.copy().get(fn_param)):
                kwargs[_param] = value

                del kwargs[fn_param]

            return fn(self, *args, **kwargs)

        return wrap_actions

    return wrapper


def _fn_has_valid_kwargs(valid_kwargs: tuple[KwargValueValidator], fn_kwargs: dict) -> NoReturn:
    """Determine if a function has a valid kwarg.
    :param valid_kwargs: tuple of KwargValueValidator objects; these are the valid kwargs for the function
    :param fn_kwargs: dictionary object containing the key word arguments of the function"""
    valid_kwarg_strs = [v.name for v in valid_kwargs]
    valids = set(_requests_kwargs).union(set(valid_kwarg_strs))

    for kw, _ in fn_kwargs.items():
        if kw not in valids:
            raise AttributeError(
                f"Error: '{kw!s}' is not a valid argument: valid function arguments are: {valid_kwarg_strs}"
            )


def validate_kwargs(*kw_validators: KwargsValidator) -> Callable:
    """Decorator that validates the kwargs provided to a method."""

    def wrapper(fn: Callable) -> Callable:
        @wraps(fn)
        def wrap_actions(self, *args, **kwargs) -> Optional[dict]:  # type: ignore
            for kwv in kw_validators:
                if kwv.valid_kwargs:
                    _fn_has_valid_kwargs(kwv.valid_kwargs, kwargs)

                    for validator in kwv.valid_kwargs:
                        if value := kwargs.get(validator.name):
                            validator.validate(value)

                if kwv.required_kwargs:
                    for validator in kwv.required_kwargs:
                        if validator.name not in kwargs:
                            raise AttributeError(f"Error: missing required argument '{validator.name!s}'")

                if kwv.conditional_kwargs:
                    c_kwargs = [validator.name for validator in kwv.conditional_kwargs]

                    if not any(kw in kwargs for kw in c_kwargs):
                        raise AttributeError(f"Error: missing one or more conditional required arguments: {c_kwargs}")

            return fn(self, *args, **kwargs)

        return wrap_actions

    return wrapper
