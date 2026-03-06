# ============================================================
# Python OOP & Decorators - Kapsamlı Örnek Koleksiyonu
# Konu: Decorators, Property, Static/Class Methods, Abstract,
#        Overloading, Final, Override
# ============================================================


# ============================================================
# SECTION 1: DECORATORS (Dekoratörler)
# ============================================================
# Dekoratörler, bir fonksiyonu sarmalayarak davranışını
# değiştiren veya genişleten fonksiyonlardır.
# Syntax: @dekorator_adi şeklinde kullanılır.
# ============================================================

print("=" * 60)
print("SECTION 1: DECORATORS")
print("=" * 60)


def my_decorator(func):
    """
    Basit bir dekoratör örneği.
    'func' parametresi sarmalanacak fonksiyonu temsil eder.
    """
    def wrapper():
        print("wrapper function executed - önce")
        func()
        print("wrapper function executed - sonra")
    return wrapper  # BUG FIX: wrapper döndürülür, çağrılmaz


@my_decorator
def hello_world():
    print("hello world")


hello_world()
# Çıktı:
# wrapper function executed - önce
# hello world
# wrapper function executed - sonra


# ============================================================
# SECTION 2: PROPERTY DECORATORS
# ============================================================
# @property: getter tanımlar — nesne.attribute sözdizimi ile
#            gizli (_private) alanlara güvenli erişim sağlar.
# @x.setter: değer atanırken doğrulama (validation) yapar.
# @x.deleter: del nesne.attribute çağrıldığında çalışır.
# Amaç: Encapsulation (veri gizleme) + veri doğrulaması.
# ============================================================

print("=" * 60)
print("SECTION 2: PROPERTY DECORATORS")
print("=" * 60)


class Person:
    def __init__(self, name, age):
        # Name mangling: __name → _Person__name
        self.__name = name
        self.__age = age

    # --- NAME ---
    @property
    def name(self):
        """Gizli __name alanını döndüren getter."""
        return self.__name

    @name.setter
    def name(self, value):
        """
        İsim ataması sırasında tip ve uzunluk doğrulaması yapar.
        BUG FIX: raise print(...) → raise ValueError(...) olarak düzeltildi.
        raise ifadesi bir exception nesnesi almalıdır, print() None döndürür.
        """
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if len(value) < 2:
            raise ValueError("Name should be at least 2 characters")
        self.__name = value

    @name.deleter
    def name(self):
        """del person.name çağrıldığında ismi None yapar."""
        self.__name = None

    # --- AGE ---
    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        """
        Yaş atamasında tip ve aralık doğrulaması.
        BUG FIX: self.__age = value satırı eksikti — setter değeri kaydetmiyordu!
        """
        if not isinstance(value, int):
            raise ValueError("age must be integer")
        if value < 0:
            raise ValueError("age must be positive")
        if value > 150:
            raise ValueError("age must be less than or equal to 150")
        self.__age = value  # BUG FIX: bu satır eksikti


ismet = Person("ismet", 18)
print(ismet.name)            # ismet
ismet.name = "ismet KEREM EREN"
print(ismet.name)            # ismet KEREM EREN
del ismet.name
print(ismet.name)            # None


# ============================================================
# SECTION 3: STATIC METHOD
# ============================================================
# @staticmethod: sınıfa ait ama ne self (instance) ne de
#                cls (class) parametresi almayan metodlar.
# Kullanım: Sınıfla mantıksal ilişkisi olan ama durumdan
#           bağımsız yardımcı (utility) fonksiyonlar için.
# ============================================================

print("=" * 60)
print("SECTION 3: STATIC METHOD")
print("=" * 60)


class MathOperations:
    @staticmethod
    def add(x, y):
        """Instance oluşturmadan doğrudan çağrılabilir."""
        return x + y


print(MathOperations.add(1, 2))   # 3


# ============================================================
# SECTION 4: CLASS METHOD
# ============================================================
# @classmethod: ilk parametre olarak cls (sınıfın kendisi) alır.
# Kullanım amacı 1 — Alternatif constructor (named constructor):
#   cls(...) çağırarak yeni instance üretir.
# Kullanım amacı 2 — Sınıf düzeyindeki state'e erişim/güncelleme.
# ============================================================

print("=" * 60)
print("SECTION 4: CLASS METHOD")
print("=" * 60)


class Pizza:
    total_pizzas = 0  # Sınıf değişkeni — tüm instance'lar paylaşır

    def __init__(self, ingredients):
        self.ingredients = ingredients
        Pizza.total_pizzas += 1

    @classmethod
    def margherita(cls):
        """Alternatif constructor: Margherita pizzası oluşturur."""
        return cls(["peynir", "domates", "fesleğen"])

    @classmethod
    def pepperoni(cls):
        """Alternatif constructor: Pepperoni pizzası oluşturur."""
        return cls(["peynir", "sucuk", "domates"])

    @classmethod
    def get_total_pizzas(cls):
        """Kaç pizza üretildiğini döndürür."""
        return cls.total_pizzas


pizza1 = Pizza.margherita()
pizza2 = Pizza.pepperoni()
print(Pizza.get_total_pizzas())   # 2


# ============================================================
# SECTION 5: ABSTRACT METHODS
# ============================================================
# ABC (Abstract Base Class): Doğrudan instance'ı alınamayan,
#   sadece miras alınmak için tasarlanmış sınıflar.
# @abstractmethod: Alt sınıfların mutlaka implement etmesi
#   gereken metodları işaretler (interface contract).
# Amaç: Polimorfizm + tutarlı API garantisi.
# ============================================================

print("=" * 60)
print("SECTION 5: ABSTRACT METHODS")
print("=" * 60)

from abc import ABC, abstractmethod


class Animal(ABC):
    def __init__(self, name):
        self.__name = name

    @abstractmethod
    def make_sound(self):
        """Her hayvanın ses çıkarma şekli farklıdır."""
        pass

    @abstractmethod
    def move(self):
        """Her hayvanın hareket şekli farklıdır."""
        pass

    @abstractmethod
    def sleep(self):
        """Her hayvanın uyku düzeni farklıdır."""
        pass


class Dog(Animal):
    """Animal'ı miras alır; tüm abstract metodları implement eder."""

    def make_sound(self):
        print("Hav hav!")

    def move(self):
        print("Köpek koştu.")

    def sleep(self):
        print("Köpek uyudu.")


barley = Dog("Barley")
barley.move()       # Köpek koştu.
barley.make_sound() # Hav hav!


# ============================================================
# SECTION 6: OVERLOADING (Tip Güvenli Aşırı Yükleme)
# ============================================================
# Python'da gerçek overloading yoktur; @overload sadece
# tip denetleyicilerine (mypy, pyright) sinyal verir.
# Gerçek çalışma mantığı tek bir uygulama metodunda yazılır.
# BUG FIX: proceess → process; metodun adı tutarsızdı.
# BUG FIX: add() zaten 0 default ile çalışıyor, değişiklik yok.
# ============================================================

print("=" * 60)
print("SECTION 6: OVERLOADING")
print("=" * 60)

from typing import overload, Union


class Calculator:
    # --- add ---
    @overload
    def add(self, a: int, b: int) -> int: ...

    @overload
    def add(self, a: int, b: int, c: int) -> int: ...

    def add(self, a: int, b: int, c: int | None = None) -> int:
        """İki veya üç sayıyı toplar."""
        if c is None:
            return a + b
        return a + b + c

    # --- process ---
    @overload
    def process(self, value: int) -> int: ...

    @overload
    def process(self, value: str) -> str: ...

    def process(self, value: Union[int, str]) -> Union[int, str]:
        """
        BUG FIX: Metod adı 'proceess' → 'process' düzeltildi.
        int gelirse 2 katını, str gelirse büyük harfe çevirir.
        """
        if isinstance(value, int):
            return value * 2
        elif isinstance(value, str):
            return value.upper()
        else:
            raise ValueError("value must be int or str")


calc = Calculator()
print(calc.add(1, 2, 0))        # 3
print(calc.process("ismet"))    # ISMET
print(calc.process(5))          # 10


# ============================================================
# SECTION 7: FINAL
# ============================================================
# @final (metod): Alt sınıfların override etmesini engeller.
#   Tip denetleyicisi (mypy) uyarı verir; runtime'da Python
#   bunu zorla engellemez (tasarım gereği uyarı amaçlıdır).
# @final (sınıf): Sınıfın miras alınmasını engeller.
# Kullanım: Kritik algoritmaları veya sabit API'leri korumak.
# ============================================================

print("=" * 60)
print("SECTION 7: FINAL")
print("=" * 60)

from typing import final


class BaseGame:
    def start(self):
        print("Game started (base)")

    @final
    def calculate_score(self, points: int) -> int:
        """
        Alt sınıflar bu metodu override edemez (tip denetleyicisi uyarır).
        BUG FIX: Kod önceden MyGame'de override ediyordu — bu @final'ı ihlal eder.
        MyGame.calculate_score kaldırıldı.
        """
        bonus = 100
        return points * bonus

    def end(self):
        print("Game ended")


class MyGame(BaseGame):
    def start(self):
        print("MyGame started!")
    # calculate_score burada OLMAMALI — @final ihlali


@final
class SecretAlgorithm:
    """Bu sınıftan miras alınamaz."""
    def process(self):
        print("Secret algorithm executed.")


game = MyGame()
game.start()
print(game.calculate_score(100))   # 10000


# ============================================================
# SECTION 8: OVERRIDE
# ============================================================
# @override: Python 3.12+ ile resmi olarak geldi.
#   Alt sınıftaki metodun gerçekten bir üst sınıf metodunu
#   override ettiğini tip denetleyicisine bildirir.
#   Yanlış yazılmış metod adlarını erken yakalar.
# BUG FIX: area() ve perimeter() __init__ içine girintilenmişti!
#   Bu yüzden sınıf metodu değil, yerel fonksiyon oluyordu.
#   Doğru girintileme ile sınıf metoduna dönüştürüldü.
# BUG FIX: Shape'deki metodlarda @override kullanımı yanlış —
#   Shape hiçbir sınıfı miras almıyor. @override kaldırıldı.
# ============================================================

print("=" * 60)
print("SECTION 8: OVERRIDE")
print("=" * 60)

from typing import override


class Shape:
    def area(self) -> float:
        return 0.0

    def perimeter(self) -> float:
        return 0.0


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    # BUG FIX: Bu metodlar önceden __init__ bloğu içindeydi
    # (fazla girintileme), sınıf metoduna alındı.
    @override
    def area(self) -> float:
        return self.width * self.height

    @override
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


rectangle = Rectangle(2, 3)
print(rectangle.area())        # 6.0
print(rectangle.perimeter())   # 10.0


# ============================================================
# BONUS SECTION 9: COMBINING DECORATORS (Dekoratör Zincirleme)
# ============================================================
# Birden fazla dekoratör üst üste uygulanabilir.
# Uygulama sırası: En alttaki dekoratör önce çalışır.
# @multiply_decorator
# @other_decorator
# def f(): ...
# → f = multiply_decorator(other_decorator(f))
# BUG FIX: multiply_decorator'da 'return wrapper' satırı
#   wrapper() içindeydi — asla çalışmıyordu, dışarı alındı.
# ============================================================

print("=" * 60)
print("BONUS SECTION 9: COMBINING DECORATORS")
print("=" * 60)


def multiply_decorator(func):
    def wrapper(x: int):
        return func(x) * 2
    return wrapper   # BUG FIX: bu satır wrapper'ın içindeydi


def other_decorator(func):
    def wrapper(x: int):
        return func(x) * 4
    return wrapper


@multiply_decorator   # 2. uygulanan → sonucu 2 ile çarpar
@other_decorator      # 1. uygulanan → sonucu 4 ile çarpar
def calculate(x: int):
    return x * 2


# Zincir: calculate(10) → 10*2=20 → *4=80 → *2=160
print(calculate(10))   # 160