from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, NoReturn, Optional, Protocol


_requests_kwargs: list[str] = [
    "method",
    "url",
    "params",
    "data",
    "headers",
    "cookies",
    "files",
    "auth",
    "timeout",
    "allow_redirects",
    "proxies",
    "hooks",
    "stream",
    "verify",
    "cert",
    "json",
]


@dataclass
class KwargValueValidator(Protocol):
    """Protocol for validating parameter values."""

    name: str
    all_digits: Optional[bool] = field(default=None)
    date_format: Optional[str] = field(default=None)
    length: Optional[int] = field(default=None)
    max_length: Optional[int] = field(default=None)
    types: Optional[type | tuple[type]] = field(default=None)
    valid_values: Optional[tuple] = field(default=None)

    def validate(self, value: Any) -> NoReturn:
        """Performs a validation action for the specified parameter value."""
        pfx = f"Error: parameter '{self.name!s}' value '{value!s}'"
        if self.types and not isinstance(value, self.types):
            raise TypeError(f"{pfx} has an unexpected type; valid type: {self.types}")

        if self.valid_values:
            if all(isinstance(v, int) for v in self.valid_values) and not isinstance(value, int):
                value = int(value)

            if all(isinstance(v, float) for v in self.valid_values) and not isinstance(value, float):
                value = float(value)

            if value not in self.valid_values:
                raise AttributeError(f"{pfx} is an invalid value; valid values {self.valid_values}")

        if self.date_format:
            try:
                datetime.strptime(value, self.date_format)
            except ValueError:
                raise ValueError(f"{pfx} does not match date format '{self.date_format}'")

        if self.length and not len(value) == self.length:
            raise ValueError(f"{pfx} must be {self.length} characters long")

        if self.all_digits and not all(chr.isdigit() for chr in value):
            raise ValueError(f"{pfx} must be all digits")

        if self.max_length and len(value) > self.max_length:
            raise ValueError(f"{pfx} must not exceed {self.max_length} characters")


@dataclass
class KwargsValidator(Protocol):
    """Protocol for validating kwargs are valid or missing required parameters."""

    valid_kwargs: tuple[KwargValueValidator]
    required_kwargs: Optional[tuple[KwargValueValidator, ...]] = field(default=None)
    conditional_kwargs: Optional[tuple[KwargValueValidator, ...]] = field(default=None)
