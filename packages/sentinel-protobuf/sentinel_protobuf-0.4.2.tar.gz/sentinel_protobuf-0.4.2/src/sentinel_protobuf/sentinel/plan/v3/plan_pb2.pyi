from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from sentinel.types.v1 import price_pb2 as _price_pb2
from sentinel.types.v1 import status_pb2 as _status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Plan(_message.Message):
    __slots__ = ('id', 'prov_address', 'gigabytes', 'hours', 'prices', 'status', 'status_at')
    ID_FIELD_NUMBER: _ClassVar[int]
    PROV_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    GIGABYTES_FIELD_NUMBER: _ClassVar[int]
    HOURS_FIELD_NUMBER: _ClassVar[int]
    PRICES_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    prov_address: str
    gigabytes: int
    hours: int
    prices: _containers.RepeatedCompositeFieldContainer[_price_pb2.Price]
    status: _status_pb2.Status
    status_at: _timestamp_pb2.Timestamp

    def __init__(self, id: _Optional[int]=..., prov_address: _Optional[str]=..., gigabytes: _Optional[int]=..., hours: _Optional[int]=..., prices: _Optional[_Iterable[_Union[_price_pb2.Price, _Mapping]]]=..., status: _Optional[_Union[_status_pb2.Status, str]]=..., status_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...