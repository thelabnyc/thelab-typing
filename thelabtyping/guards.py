from collections.abc import Callable
from typing import _LiteralGenericAlias  # type:ignore[attr-defined]
from typing import (
    TypeAliasType,
    TypeIs,
    get_args,
)


def is_literal_factory[T](lit: T) -> Callable[[object], TypeIs[T]]:
    """
    Given a `Literal` type, return a TypeIs type guard to determine if a
    variable is a member of that Literal. Example usage:

    >>> from typing import Literal
    >>> type MyLiteral = Literal["foo", "bar"]
    >>> is_literal = is_literal_factory(MyLiteral)
    >>> is_literal("foo")
    True
    >>> is_literal("FOO")
    False
    """

    def is_literal(arg: object) -> TypeIs[T]:
        """
        Type guard which narrows a type down to being a member of a Literal
        """
        # If the literal was defined with the `type` keyword, then we need to
        # force it to resolve by getting __value__.
        resolved_lit: object = lit
        if isinstance(resolved_lit, TypeAliasType):
            resolved_lit = resolved_lit.__value__
        assert isinstance(resolved_lit, _LiteralGenericAlias)
        return arg in get_args(resolved_lit)

    return is_literal
