from math import gcd

class RationalError(ZeroDivisionError): pass
class RationalValueError(Exception): pass

class Rational:
    def __init__(self, *args):
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, Rational):
                self.n, self.d = arg.n, arg.d
            elif isinstance(arg, str):
                self.n, self.d = map(int, arg.split('/'))
            elif isinstance(arg, int):
                self.n, self.d = arg, 1
            else:
                raise RationalValueError("Некоректні аргументи конструктора.")
        elif len(args) == 2:
            self.n, self.d = args
        else:
            raise RationalValueError("Некоректні аргументи конструктора.")

        if self.d == 0:
            raise RationalError("Знаменник не може дорівнювати нулю.")

        g = gcd(self.n, self.d)
        self.n //= g
        self.d //= g
        if self.d < 0:
            self.n, self.d = -self.n, -self.d

    @staticmethod
    def _to_rational(value):
        return value if isinstance(value, Rational) else Rational(value)

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
        if other.n == 0: raise RationalError("Ділення на нуль.")
        return Rational(self.n * other.d, self.d * other.n)

    def __call__(self):
        return self.n / self.d

    def __getitem__(self, key):
        if key == "n": return self.n
        if key == "d": return self.d
        raise KeyError("Ключ має бути 'n' або 'd'.")

    def __setitem__(self, key, value):
        if key == "n":
            self.n = value
        elif key == "d":
            if value == 0: raise RationalError("Знаменник не може бути нулем.")
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
        try:
            self.data.append(Rational(value))
        except Exception:
            raise RationalValueError("До списку можна додавати лише Rational, int або рядок виду 'n/d'.")

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
    r3 = Rational("3/0")

except RationalError as e:
    print("RationalError:", e)
except RationalValueError as e:
    print("RationalValueError:", e)
