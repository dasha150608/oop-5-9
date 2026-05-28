from math import gcd


class RationalError(ZeroDivisionError):
    pass


class RationalValueError(Exception):
    pass


class Rational:

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], Rational):
            self.n, self.d = args[0].n, args[0].d
        elif len(args) == 1 and isinstance(args[0], str):
            try:
                n, d = map(int, args[0].split("/"))
            except ValueError:
                raise RationalValueError("Некоректний формат рядка.")
            if d == 0:
                raise RationalError("Знаменник не може дорівнювати нулю.")
            self.n, self.d = n, d
        elif len(args) == 2:
            n, d = args
            if not (isinstance(n, int) and isinstance(d, int)):
                raise RationalValueError("Чисельник і знаменник мають бути цілими.")
            if d == 0:
                raise RationalError("Знаменник не може дорівнювати нулю.")
            self.n, self.d = n, d
        else:
            raise RationalValueError("Некоректні аргументи конструктора.")

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
        return f"{self.n}/{self.d}"


class RationalList:

    def __init__(self):
        self.data = []

    def append(self, value):
        if isinstance(value, Rational):
            self.data.append(value)
        elif isinstance(value, (int, str)):
            self.data.append(Rational(value))
        else:
            raise RationalValueError(
                "До списку можна додавати лише Rational, int або рядок виду 'n/d'."
            )

    def __str__(self):
        return "[" + ", ".join(str(x) for x in self.data) + "]"


try:
    r1 = Rational(2, 4)
    r2 = Rational("3/5")
    print(r1)
    print(r2)
    print(r1 + r2)
    print(r1 - 1)
    print(r1 * 2)
    print(r2 / r1)
    print(r1())
    print(r1["n"])
    print(r1["d"])
    r1["n"] = 10
    print(r1)

    lst = RationalList()
    lst.append(r1)
    lst.append(5)
    lst.append("7/8")
    print(lst)
    lst.append([1, 2])
except (RationalError, RationalValueError) as e:
    print(f"{type(e).__name__}: {e}")
