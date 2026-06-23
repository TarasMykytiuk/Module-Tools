from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List
import random
import math

class OperatingSystem(Enum):
    MACOS = "macOS"
    ARCH = "Arch Linux"
    UBUNTU = "Ubuntu"

systems_list = list(OperatingSystem)

@dataclass(frozen=True)
class Person:
    name: str
    age: int
    # Sorted in order of preference, most preferred is first.
    preferred_operating_system: List[OperatingSystem]
    
    def __hash__(self):
        return hash((self.name, self.age))


@dataclass(frozen=True)
class Laptop:
    id: int
    manufacturer: str
    model: str
    screen_size_in_inches: float
    operating_system: OperatingSystem

def allocate_laptops(people: List[Person], laptops: List[Laptop], is_pre_sort, is_randomized) -> Dict[Person, Laptop]:
    if len(people) > len(laptops):
        raise Exception("Sorry, there are not enough laptops.")
    alloc_dict = {}
    # people with fewer options choose first, because they potentially can generate most sadness
    if is_pre_sort:
        people.sort(key=lambda person: len(person.preferred_operating_system))
    elif is_randomized:
        random.shuffle(people)
    for person in people:
        for laptop in laptops:
            is_match = False
            # if it a last chance to get a laptop, it used anyway
            if laptops.index(laptop) == len(laptops) - 1:
                alloc_dict[person] = laptop
                break
            for sys in person.preferred_operating_system:
                if sys == laptop.operating_system:
                    alloc_dict[person] = laptop
                    laptops.pop(laptops.index(laptop))
                    is_match = True
                    break
            if is_match:
                break
    return alloc_dict

def calcSadness(person: Person, laptop: Laptop) -> int:
    sadness = 0
    is_sys_matched = False
    for i in range(len(person.preferred_operating_system)):
        if person.preferred_operating_system[i] == laptop.operating_system:
            is_sys_matched = True
            sadness += i
            break
    if not is_sys_matched:
        sadness = 100
    return sadness

def print_allocation(alloc_dict: Dict[Person, Laptop]) -> None:
    for person in alloc_dict.keys():
        print(f"{person.name} gets: {alloc_dict[person].model} with {alloc_dict[person].operating_system.name}.")

def generatePersons(quantity):
    persons = []
    for i in range(quantity):
        name = "name_" + str(i)
        age = random.randint(0, 100)
        pref_sys_num = random.randint(1, 3)
        pref_systems = []
        for j in range(pref_sys_num):
            while True:
                sys = random.choice(systems_list)
                if sys not in pref_systems:
                    pref_systems.append(sys)
                    break
        person = Person(name=name, age=age, preferred_operating_system=pref_systems)
        persons.append(person)
    return persons

def generateLaptops(quantity):
    laptops = []
    for i in range(quantity):
        id = i
        sys = random.choice(systems_list)
        laptop = Laptop(
            id=id,
            manufacturer="manufacturer",
            model="model",
            screen_size_in_inches=14.2,
            operating_system=sys,
        )
        laptops.append(laptop)
    return laptops

def main() -> None:
    persons = generatePersons(100)
    laptops = generateLaptops(100)
    test_iterations = 100
    # calculate average sadness with original persons list with one iteration
    result_dict_50 = allocate_laptops(
        people=persons.copy(), laptops=laptops.copy(), is_pre_sort=False, is_randomized=False,
    )
    original_sadness = 0
    for person in result_dict_50.keys():
        original_sadness += calcSadness(person, result_dict_50[person])
    # calculate average sadness with pre_sorted persons list
    result_dict_50 = allocate_laptops(
        people=persons.copy(), laptops=laptops.copy(), is_pre_sort=True, is_randomized=False
    )
    pre_sorted_sadness = 0
    for person in result_dict_50.keys():
        pre_sorted_sadness += calcSadness(person, result_dict_50[person])
    # calculate average sadness with randomized persons list
    tot_rand_sad = 0
    rand_variants = []
    for i in range(test_iterations):
        result_dict_50 = allocate_laptops(
            people=persons.copy(), laptops=laptops.copy(), is_pre_sort=False, is_randomized=True
        )
        rand_sadness = 0
        for person in result_dict_50.keys():
            rand_sadness += calcSadness(person, result_dict_50[person])
        rand_variants.append([rand_sadness, result_dict_50])
        tot_rand_sad += rand_sadness
    # fund allocation with a minimum sadness among random variants
    min_sadness_value = math.inf
    min_sadness_allocation = []
    for variant in rand_variants:
        if variant[0] < min_sadness_value:
            min_sadness_value = variant[0]
            min_sadness_allocation = variant[1]

    print(f"Original one-time allocated sadness: {original_sadness}")
    print(f"Pre sorted sadness: {pre_sorted_sadness}")
    print(f"Minimum randomized sadness: {min_sadness_value}")
    print(f"Average randomized sadness: {tot_rand_sad/test_iterations}")


if __name__ == "__main__":
    main()
