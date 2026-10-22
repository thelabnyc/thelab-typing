from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest
import pydantic

from .serializers import Empty

"""
Alias for any user: e.g. maybe authenticated, maybe not.
"""
type AnyUser = User | AnonymousUser


class TypedRequest[
    QST: pydantic.BaseModel,  # QueryString Type
    BT: pydantic.BaseModel,  # Body Type
    UT: AnyUser = AnyUser,  # User Type
](HttpRequest):
    """
    Wrapper around the stock HttpRequest class. Provides typed-checked,
    validated (via Pydantic) data models for the querystring, the request body,
    or both. Can also assert (and type) that the user is authenticated.
    """

    user: UT

    __validated_querystring: QST
    __validated_body: BT

    def __init__(self, request: HttpRequest, user: UT, qs: QST, body: BT) -> None:
        # Clone the original request into self
        self.__dict__.update(request.__dict__)
        # Add the validate request data objects
        self.user = user
        self.__validated_querystring = qs
        self.__validated_body = body

    @property
    def validated_querystring(self) -> QST:
        """
        Return the fully-validated querystring data. This is a property merely
        to avoid accidental mutation.
        """
        return self.__validated_querystring

    @property
    def validated_body(self) -> BT:
        """
        Return the fully-validated body (POST/PUT/etc) data. This is a property
        merely to avoid accidental mutation.
        """
        return self.__validated_body


"""
Alias for defining a TypedRequest with a validated querystring and an empty
body.
"""
type TypedRequestQuery[
    _QST: pydantic.BaseModel,
    _UT: AnyUser = AnyUser,
] = TypedRequest[_QST, Empty, _UT]

"""
Alias for defining a TypedRequest with an empty querystring and an validated
body.
"""
type TypedRequestBody[
    _BT: pydantic.BaseModel,
    _UT: AnyUser = AnyUser,
] = TypedRequest[Empty, _BT, _UT]

"""
Alias for defining a TypedRequest with an empty querystring and an empty body.
"""
type EmptyTypedRequest[
    _UT: AnyUser = AnyUser,
] = TypedRequest[Empty, Empty, _UT]


"""
Alias for defining a TypedRequest with a empty querystring, a validated body,
and and authenticated user.
"""
type AuthdTypedRequest[
    _QST: pydantic.BaseModel,
    _BT: pydantic.BaseModel,
    _UT: User = User,
] = TypedRequest[_QST, _BT, _UT]

"""
Alias for defining a TypedRequest with a validated querystring, an empty body,
and and authenticated user.
"""
type AuthdTypedRequestQuery[
    _QST: pydantic.BaseModel,
    _UT: User = User,
] = TypedRequest[_QST, Empty, _UT]

"""
Alias for defining a TypedRequest with a empty querystring, a validated body,
and and authenticated user.
"""
type AuthdTypedRequestBody[
    _BT: pydantic.BaseModel,
    _UT: User = User,
] = TypedRequest[Empty, _BT, _UT]

"""
Alias for defining a TypedRequest with a empty querystring, an empty body,
and and authenticated user.
"""
type AuthdEmptyTypedRequest[
    _UT: User = User,
] = TypedRequest[Empty, Empty, _UT]
