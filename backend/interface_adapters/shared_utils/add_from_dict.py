from dataclasses import fields
from typing import Any, Type, TypeVar


T = TypeVar('T')

def add_from_dict(cls: Type[T]) -> Type[T]:
    """
    The decorator that add add_from_dict method to a dataclass
    in order to be able to create an instance of such dataclass
    if the number of properties in dict exceed the number of
    properties in dataclass.
    """
    def from_dict(cls: Type[T], data: dict[str, Any]) -> T:
        existing = {field.name for field in fields(cls)}
        incoming = {key: value for key, value in data.items() if key in existing}
        return cls(**incoming)
    
    setattr(cls, 'from_dict', classmethod(from_dict))
    return cls
