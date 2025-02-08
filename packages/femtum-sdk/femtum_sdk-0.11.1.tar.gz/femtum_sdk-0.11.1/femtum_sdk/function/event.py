from typing import Optional, TypedDict


class TagDict(TypedDict):
    Key: str
    Value: Optional[str]


class FunctionConfigurationDict(TypedDict):
    WaferName: Optional[str]
    ReticleName: Optional[str]
    DieName: Optional[str]
    CircuitName: Optional[str]
    ResultName: Optional[str]
    Tags: list[TagDict]


class FunctionHandleEventDict(TypedDict):
    Configuration: FunctionConfigurationDict


class EventParser:
    def __init__(self, event: FunctionHandleEventDict):
        self.event = event

    def find(self, key: str):
        return self.event.get(key)

    def find_int(self, key: str, fallback: Optional[int] = None) -> int:
        value = self.event.get(key)
        value = int(value) if value is not None else None

        if fallback is not None and value is None:
            return fallback
        if value is None:
            raise ValueError(f"Missing required field '{key}'")

        return value

    def find_float(self, key: str, fallback: Optional[int] = None) -> float:
        value = self.event.get(key)
        value = float(value) if value is not None else None

        if fallback is not None and value is None:
            return fallback
        if value is None:
            raise ValueError(f"Missing required field '{key}'")

        return value

    def find_int_list(self, key: str, fallback: list[int] = None) -> list[int]:
        value = self.event.get(key)

        if value is not None:
            return [int(v) for v in value]

        if fallback is not None:
            return fallback

        return []

    def find_float_list(self, key: str, fallback: list[float] = None) -> list[float]:
        value = self.event.get(key)

        if value is not None:
            return [float(v) for v in value]

        if fallback is not None:
            return fallback

        return []
