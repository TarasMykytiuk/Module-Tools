from datetime import date
# function is an independent reusable block of code.
# method is a function that belongs to a class.
# .is_adult() belongs to Person class --> it is a method.

class Person:

    def __init__(self, name: str, date_of_birth: date):
        self.name = name
        self.date_of_birth = date_of_birth

    def is_adult(self) -> bool:
        current_date = date.today()
        full_years = current_date.year - self.date_of_birth.year
        if (current_date.month, current_date.day) < (self.date_of_birth.month, self.date_of_birth.day):
            full_years -= 1
        return full_years >= 18


imran = Person("Imran", date(2008, 1, 30))
eliza = Person("Eliza", date(2088, 7, 30))
someone = Person("Someone", date(2021, 7, 30))
print("Imran is adult: " + str(imran.is_adult()))
print("Eliza is adult: " + str(eliza.is_adult()))
print("Someone is adult: " + str(someone.is_adult()))
