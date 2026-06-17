from enum import Enum

from dataclasses import dataclass
import sys
from typing import List


class OperatingSystem(Enum):
    MACOS = "macOS"
    ARCH = "Arch Linux"
    UBUNTU = "Ubuntu"


@dataclass(frozen=True)
class Person:
    name: str
    age: int
    preferred_operating_system: OperatingSystem


@dataclass(frozen=True)
class Laptop:
    id: int
    manufacturer: str
    model: str
    screen_size_in_inches: float
    operating_system: OperatingSystem


def find_possible_laptops(laptops: List[Laptop], person: Person) -> List[Laptop]:
    possible_laptops = []
    for laptop in laptops:
        if laptop.operating_system == person.preferred_operating_system:
            possible_laptops.append(laptop)
    return possible_laptops


def operating_system_laptop_num(
    laptops: List[Laptop], system: OperatingSystem
) -> List[Laptop]:
    sys_laptops = []
    for laptop in laptops:
        if laptop.operating_system == system:
            sys_laptops.append(laptop)
    return sys_laptops


def inputPerson() -> dict:
    name = input("Enter name: ")
    age = 0
    system = None
    while True:
        try:
            age = int(input("Enter age: "))
            break
        except:
            print("Age must be a number.")
    while True:
        systemStr = input("Enter preferred operating system: ")
        for system_variant in OperatingSystem:
            if systemStr.lower() == system_variant.name.lower():
                system = system_variant
        if system == None:
            systems = ", ".join(os.value for os in OperatingSystem)
            print("Incorrect operating system input. Select from: " + systems)
        else:
            break

    return {"name": name, "age": age, "system": system}


def main():
    input = inputPerson()

    newPerson = Person(input["name"], input["age"], input["system"])
    laptops = [
        Laptop(
            id=1,
            manufacturer="Dell",
            model="XPS",
            screen_size_in_inches=13,
            operating_system=OperatingSystem.ARCH,
        ),
        Laptop(
            id=2,
            manufacturer="Dell",
            model="XPS",
            screen_size_in_inches=15,
            operating_system=OperatingSystem.UBUNTU,
        ),
        Laptop(
            id=3,
            manufacturer="Dell",
            model="XPS",
            screen_size_in_inches=15,
            operating_system=OperatingSystem.UBUNTU,
        ),
        Laptop(
            id=4,
            manufacturer="Apple",
            model="macBook",
            screen_size_in_inches=13,
            operating_system=OperatingSystem.MACOS,
        ),
    ]

    preferred_laptops_num = len(find_possible_laptops(laptops, newPerson))
    max_other_laptops = 0
    other_laptops_sys = None
    for system_variant in OperatingSystem:
        if system_variant == input["system"]:
            continue
        laptops_num = len(operating_system_laptop_num(laptops, system_variant))
        if laptops_num > preferred_laptops_num:
            max_other_laptops = laptops_num
            other_laptops_sys = system_variant

    print(
        "We have "
        + str(preferred_laptops_num)
        + " with "
        + input["system"].name
        + " installed."
    )
    if max_other_laptops > 0:
        print(
            "We also have "
            + str(max_other_laptops)
            + " with "
            + other_laptops_sys.name
            + " installed."
        )


if __name__ == "__main__":
    main()
