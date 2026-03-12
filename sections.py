from pydantic import BaseModel
from enum import Enum
import json

class units(Enum):
    ticks = "ticks"
    ms = "ms"
    s = "s"
    ns = "ns"

class SecOrder(Enum):
    const = "const"
    linear = "linear"
    square = "square"
    cubic = "cubic"
    
class SecDO(BaseModel):
    value: bool
    duration: float
    units: units

    def to_json(self) -> json:
        return self.model_dump_json()


class SecAO(BaseModel):
    yl: float
    yr: float
    dl: float
    dr: float
    t: float
    units: units
    order: SecOrder

    def to_json(self) -> json:
        return self.model_dump_json()


class Stack[T]:
    def __init__(self) -> None:
        # Create an empty list with items of type T
        self.items: list[T] = []

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()

    def empty(self) -> bool:
        return not self.items

class SecStack[T: (SecDO, SecAO)](Stack[T]):
    def show(self)-> str:
        s = ""
        for item in self.items:
            s += item.to_json()
        return s

def main():
    secdo = SecDO(value=False, duration=100.0, units=units.ms)

    secao = SecAO(yl=0,yr=1,dl=1,dr=1, t=100, duration=100.0, units=units.ms, order=SecOrder.const)


    a = SecStack[SecAO]()
    a.push(secao)
    a.push(secao)
    print(a.show())

    e = SecStack[SecDO]()
    e.push(secdo)
    e.push(secdo)
    print(e.show())

if __name__ == "__main__":
    main()


    



