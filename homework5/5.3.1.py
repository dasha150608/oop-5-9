from math import gcd


class RationalError(ZeroDivisionError):
    pass


class RationalValueError(Exception):
    pass


class Rational:
    def __init__(self, *args):
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, Rational):
                self.n, self.d = arg.n, arg.d
            elif isinstance(arg, str):
                try:
                    self.n, self.d = map(int, arg.split("/"))
                except ValueError:
                    raise RationalValueError("Некоректний формат рядка.")
            elif isinstance(arg, int):
                self.n, self.d = arg, 1
            else:
                raise RationalValueError("Некоректні аргументи.")
        elif len(args) == 2:
            self.n, self.d = args
            if not (isinstance(self.n, int) and isinstance(self.d, int)):
                raise RationalValueError("Чисельник і знаменник мають бути цілими.")
        else:
            raise RationalValueError("Некоректні аргументи.")

        if self.d == 0:
            raise RationalError("Знаменник не може дорівнювати нулю.")

        g = gcd(self.n, self.d)
        self.n //= g
        self.d //= g
        if self.d < 0:
            self.n, self.d = -self.n, -self.d

    @staticmethod
    def _to_rational(value):
        if isinstance(value, Rational):
            return value
        if isinstance(value, int):
            return Rational(value, 1)
        raise RationalValueError("Операнд має бути Rational або int.")

    def __add__(self, other):
        other = self._to_rational(other)
        return Rational(self.n * other.d + other.n * self.d, self.d * other.d)

    def __sub__(self, other):
        other = self._to_rational(other)
        return Rational(self.n * other.d - other.n * self.d, self.d * other.d)

    def __mul__(self, other):
        other = self._to_rational(other)
        return Rational(self.n * other.n, self.d * other.d)

    def __truediv__(self, other):
        other = self._to_rational(other)
        if other.n == 0:
            raise RationalError("Ділення на нуль.")
        return Rational(self.n * other.d, self.d * other.n)

    def __call__(self):
        return self.n / self.d

    def __getitem__(self, key):
        if key == "n":
            return self.n
        if key == "d":
            return self.d
        raise KeyError("Ключ має бути 'n' або 'd'.")

    def __setitem__(self, key, value):
        if not isinstance(value, int):
            raise RationalValueError("Значення має бути цілим.")
        if key == "n":
            self.n = value
        elif key == "d":
            if value == 0:
                raise RationalError("Знаменник не може бути нулем.")
            self.d = value
        else:
            raise KeyError("Ключ має бути 'n' або 'd'.")

        g = gcd(self.n, self.d)
        self.n //= g
        self.d //= g

    def __str__(self):
        return str(self.n) if self.d == 1 else f"{self.n}/{self.d}"


def evaluate_expressions_from_file(filename="input01.txt"):
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            expr = line.strip()
            if not expr:
                continue

            tokens = []
            for t in expr.split():
                if t in ("+", "-", "*", "/"):
                    tokens.append(t)
                else:
                    tokens.append(f"Rational('{t}')" if "/" in t else f"Rational({t})")

            result = eval(" ".join(tokens))
            print(result())


if __name__ == "__main__":
    evaluate_expressions_from_file()
