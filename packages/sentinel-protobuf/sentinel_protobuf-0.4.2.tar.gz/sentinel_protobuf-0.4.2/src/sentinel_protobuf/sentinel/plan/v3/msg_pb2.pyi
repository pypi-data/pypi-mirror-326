from gogoproto import gogo_pb2 as _gogo_pb2
from sentinel.types.v1 import price_pb2 as _price_pb2
from sentinel.types.v1 import renewal_pb2 as _renewal_pb2
from sentinel.types.v1 import status_pb2 as _status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class MsgCreatePlanRequest(_message.Message):
    __slots__ = ('frm', 'gigabytes', 'hours', 'prices')
    FRM_FIELD_NUMBER: _ClassVar[int]
    GIGABYTES_FIELD_NUMBER: _ClassVar[int]
    HOURS_FIELD_NUMBER: _ClassVar[int]
    PRICES_FIELD_NUMBER: _ClassVar[int]
    frm: str
    gigabytes: int
    hours: int
    prices: _containers.RepeatedCompositeFieldContainer[_price_pb2.Price]

    def __init__(self, frm: _Optional[str]=..., gigabytes: _Optional[int]=..., hours: _Optional[int]=..., prices: _Optional[_Iterable[_Union[_price_pb2.Price, _Mapping]]]=...) -> None:
        ...

class MsgLinkNodeRequest(_message.Message):
    __slots__ = ('frm', 'id', 'node_address')
    FRM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    frm: str
    id: int
    node_address: str

    def __init__(self, frm: _Optional[str]=..., id: _Optional[int]=..., node_address: _Optional[str]=...) -> None:
        ...

class MsgUnlinkNodeRequest(_message.Message):
    __slots__ = ('frm', 'id', 'node_address')
    FRM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    frm: str
    id: int
    node_address: str

    def __init__(self, frm: _Optional[str]=..., id: _Optional[int]=..., node_address: _Optional[str]=...) -> None:
        ...

class MsgUpdatePlanStatusRequest(_message.Message):
    __slots__ = ('frm', 'id', 'status')
    FRM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    frm: str
    id: int
    status: _status_pb2.Status

    def __init__(self, frm: _Optional[str]=..., id: _Optional[int]=..., status: _Optional[_Union[_status_pb2.Status, str]]=...) -> None:
        ...

class MsgStartSessionRequest(_message.Message):
    __slots__ = ('frm', 'id', 'denom', 'renewal_price_policy', 'node_address')
    FRM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    DENOM_FIELD_NUMBER: _ClassVar[int]
    RENEWAL_PRICE_POLICY_FIELD_NUMBER: _ClassVar[int]
    NODE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    frm: str
    id: int
    denom: str
    renewal_price_policy: _renewal_pb2.RenewalPricePolicy
    node_address: str

    def __init__(self, frm: _Optional[str]=..., id: _Optional[int]=..., denom: _Optional[str]=..., renewal_price_policy: _Optional[_Union[_renewal_pb2.RenewalPricePolicy, str]]=..., node_address: _Optional[str]=...) -> None:
        ...

class MsgCreatePlanResponse(_message.Message):
    __slots__ = ('id',)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int

    def __init__(self, id: _Optional[int]=...) -> None:
        ...

class MsgLinkNodeResponse(_message.Message):
    __slots__ = ()

    def __init__(self) -> None:
        ...

class MsgUnlinkNodeResponse(_message.Message):
    __slots__ = ()

    def __init__(self) -> None:
        ...

class MsgUpdatePlanStatusResponse(_message.Message):
    __slots__ = ()

    def __init__(self) -> None:
        ...

class MsgStartSessionResponse(_message.Message):
    __slots__ = ('id',)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int

    def __init__(self, id: _Optional[int]=...) -> None:
        ...