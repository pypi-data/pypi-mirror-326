from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Channel(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DoublePoint(_message.Message):
    __slots__ = ["timestamp", "value"]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    value: float
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., value: _Optional[float] = ...) -> None: ...

class DoublePoints(_message.Message):
    __slots__ = ["points"]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[DoublePoint]
    def __init__(self, points: _Optional[_Iterable[_Union[DoublePoint, _Mapping]]] = ...) -> None: ...

class Points(_message.Message):
    __slots__ = ["double_points", "string_points"]
    DOUBLE_POINTS_FIELD_NUMBER: _ClassVar[int]
    STRING_POINTS_FIELD_NUMBER: _ClassVar[int]
    double_points: DoublePoints
    string_points: StringPoints
    def __init__(self, double_points: _Optional[_Union[DoublePoints, _Mapping]] = ..., string_points: _Optional[_Union[StringPoints, _Mapping]] = ...) -> None: ...

class Series(_message.Message):
    __slots__ = ["channel", "points", "tags"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    channel: Channel
    points: Points
    tags: _containers.ScalarMap[str, str]
    def __init__(self, channel: _Optional[_Union[Channel, _Mapping]] = ..., tags: _Optional[_Mapping[str, str]] = ..., points: _Optional[_Union[Points, _Mapping]] = ...) -> None: ...

class StringPoint(_message.Message):
    __slots__ = ["timestamp", "value"]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    value: str
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., value: _Optional[str] = ...) -> None: ...

class StringPoints(_message.Message):
    __slots__ = ["points"]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[StringPoint]
    def __init__(self, points: _Optional[_Iterable[_Union[StringPoint, _Mapping]]] = ...) -> None: ...

class WriteRequestNominal(_message.Message):
    __slots__ = ["series"]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    series: _containers.RepeatedCompositeFieldContainer[Series]
    def __init__(self, series: _Optional[_Iterable[_Union[Series, _Mapping]]] = ...) -> None: ...
