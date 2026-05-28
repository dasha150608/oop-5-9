class CustomList:
    def __init__(self, items=None):
        self.data = []

        if items:
            for item in items:
                if not isinstance(item, int):
                    raise TypeError("Список може містити лише цілі числа")
                self.data.append(item)

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        if not isinstance(value, int):
            raise TypeError("Можна додавати лише цілі числа")

        self.data[index] = value

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return item in self.data

    def __iadd__(self, other):
        if isinstance(other, int):
            self.data.append(other)

        elif isinstance(other, CustomList):
            self.data.extend(other.data)

        else:
            raise TypeError("Неправильний тип операнда")

        return self

    def __isub__(self, other):
        if isinstance(other, int):
            remove_values = [other]

        elif isinstance(other, CustomList):
            remove_values = other.data

        else:
            raise TypeError("Неправильний тип операнда")

        self.data = [x for x in self.data if x not in remove_values]

        return self

    def __imul__(self, other):
        if not isinstance(other, int):
            raise TypeError("Множник має бути цілим числом")

        self.data *= other
        return self

    def __iter__(self):
        return CustomListIterator(self.data)

    def __str__(self):
        return str(self.data)



class CustomListIterator:
    def __init__(self, data):

        odd_numbers = sorted([x for x in data if x % 2 != 0])

        even_numbers = sorted(
            [x for x in data if x % 2 == 0],
            reverse=True
        )

        self.items = odd_numbers + even_numbers

        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):

        if self.index >= len(self.items):
            raise StopIteration

        value = self.items[self.index]
        self.index += 1

        return value

filename = "numbers.txt"

try:
    with open(filename, "r", encoding="utf-8") as file:

        numbers = []

        for line in file:
            parts = line.split()

            for item in parts:
                numbers.append(int(item))

    custom_list = CustomList(numbers)

    print("Вміст списку:")
    print(custom_list)

    print("\nІтерація за правилом:")
    print("1) Непарні за зростанням")
    print("2) Парні за спаданням\n")

    for number in custom_list:
        print(number, end=" ")

except FileNotFoundError:
    print("Файл не знайдено")

except ValueError:
    print("Файл містить некоректні дані")
