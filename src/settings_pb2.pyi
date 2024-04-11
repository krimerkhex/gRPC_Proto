from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Aligment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Ally: _ClassVar[Aligment]
    Enemy: _ClassVar[Aligment]

class ShipType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Corvette: _ClassVar[ShipType]
    Frigate: _ClassVar[ShipType]
    Cruiser: _ClassVar[ShipType]
    Destroyer: _ClassVar[ShipType]
    Carrier: _ClassVar[ShipType]
    Dreadnought: _ClassVar[ShipType]
Ally: Aligment
Enemy: Aligment
Corvette: ShipType
Frigate: ShipType
Cruiser: ShipType
Destroyer: ShipType
Carrier: ShipType
Dreadnought: ShipType

class Coordinate(_message.Message):
    __slots__ = ("point1", "point2", "point3", "point4", "point5", "point6")
    POINT1_FIELD_NUMBER: _ClassVar[int]
    POINT2_FIELD_NUMBER: _ClassVar[int]
    POINT3_FIELD_NUMBER: _ClassVar[int]
    POINT4_FIELD_NUMBER: _ClassVar[int]
    POINT5_FIELD_NUMBER: _ClassVar[int]
    POINT6_FIELD_NUMBER: _ClassVar[int]
    point1: float
    point2: float
    point3: float
    point4: float
    point5: float
    point6: float
    def __init__(self, point1: _Optional[float] = ..., point2: _Optional[float] = ..., point3: _Optional[float] = ..., point4: _Optional[float] = ..., point5: _Optional[float] = ..., point6: _Optional[float] = ...) -> None: ...

class Officer(_message.Message):
    __slots__ = ("first_name", "last_name", "rank")
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    first_name: str
    last_name: str
    rank: str
    def __init__(self, first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., rank: _Optional[str] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ("aligment", "name", "classs", "length", "crew_size", "armed", "officer")
    ALIGMENT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CLASSS_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    CREW_SIZE_FIELD_NUMBER: _ClassVar[int]
    ARMED_FIELD_NUMBER: _ClassVar[int]
    OFFICER_FIELD_NUMBER: _ClassVar[int]
    aligment: Aligment
    name: str
    classs: ShipType
    length: int
    crew_size: int
    armed: bool
    officer: _containers.RepeatedCompositeFieldContainer[Officer]
    def __init__(self, aligment: _Optional[_Union[Aligment, str]] = ..., name: _Optional[str] = ..., classs: _Optional[_Union[ShipType, str]] = ..., length: _Optional[int] = ..., crew_size: _Optional[int] = ..., armed: bool = ..., officer: _Optional[_Iterable[_Union[Officer, _Mapping]]] = ...) -> None: ...
