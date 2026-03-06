# 🐍 Python OOP & Decorators — Kapsamlı Rehber

> Python'da dekoratörler, özellik yönetimi, soyut sınıflar ve ileri OOP kavramlarını açıklayan örnek koleksiyonu.

---

## 📋 İçindekiler

1. [Decorators (Dekoratörler)](#1-decorators)
2. [Property Decorators](#2-property-decorators)
3. [Static Method](#3-static-method)
4. [Class Method](#4-class-method)
5. [Abstract Methods](#5-abstract-methods)
6. [Overloading](#6-overloading)
7. [Final](#7-final)
8. [Override](#8-override)
9. [Combining Decorators](#9-combining-decorators)
10. [Düzeltilen Hatalar (Bug Fix Özeti)](#-düzeltilen-hatalar)

---

## 1. Decorators

### Kavram
Dekoratörler, bir fonksiyonu **sarmalayarak** (wrapping) davranışını değiştiren veya genişleten fonksiyonlardır. `@dekorator` sözdizimi, `fonksiyon = dekorator(fonksiyon)` ifadesinin kısaltmasıdır.

### Yapı
```
my_decorator(func)
    └─ wrapper()          ← asıl sarmalayıcı
          ├─ önce çalış
          ├─ func()       ← orijinal fonksiyon
          └─ sonra çalış
    return wrapper        ← wrapper döndürülür, ÇAĞRILMAZ
```

### Kullanım Alanları
- Loglama (logging)
- Yetki/kimlik kontrolü (authentication)
- Performans ölçümü (timing)
- Cache/memoization

### Örnek
```python
def my_decorator(func):
    def wrapper():
        print("önce")
        func()
        print("sonra")
    return wrapper  # ← wrapper() değil, wrapper

@my_decorator
def hello_world():
    print("hello world")

hello_world()
# önce
# hello world
# sonra
```

> ⚠️ **Sık Yapılan Hata:** `return wrapper()` yazmak — parantez eklenmemelidir. `wrapper()` yazmak fonksiyonu hemen çağırır ve sonucunu (genellikle `None`) döndürür.

---

## 2. Property Decorators

### Kavram
`@property` dekoratörü, bir metodu **sözde-attribute** (pseudo-attribute) gibi kullanmayı sağlar. Getter, setter ve deleter üçlüsü ile **encapsulation** (veri gizleme) gerçekleştirilir.

| Dekoratör | Amaç |
|---|---|
| `@property` | Getter — değer okuma |
| `@x.setter` | Setter — değer atama + doğrulama |
| `@x.deleter` | Deleter — değeri silme/sıfırlama |

### Neden Kullanılır?
- Dışarıdan doğrudan `obj.__name = "x"` erişimini engeller
- Değer atamalarında **veri doğrulaması (validation)** yapar
- Gelecekte iç yapıyı değiştirirken API'yi bozmaz

### Örnek
```python
class Person:
    def __init__(self, name, age):
        self.__name = name   # name mangling: _Person__name
        self.__age = age

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")   # raise ValueError, raise print değil!
        if len(value) < 2:
            raise ValueError("Name too short")
        self.__name = value

    @name.deleter
    def name(self):
        self.__name = None
```

> ⚠️ **Sık Yapılan Hata 1:** `raise print("mesaj")` yazmak — `print()` her zaman `None` döndürür, bu yüzden `raise None` çalışır gibi görünse de `TypeError` fırlatır. Doğrusu: `raise ValueError("mesaj")`.
>
> ⚠️ **Sık Yapılan Hata 2:** `@age.setter` içinde `self.__age = value` satırını unutmak — setter değeri kaydetmezse atama hiçbir işe yaramaz.

---

## 3. Static Method

### Kavram
`@staticmethod` ile tanımlanan metodlar ne `self` (instance) ne de `cls` (class) parametresi alır. Sınıfla **mantıksal olarak ilişkili** ancak instance veya sınıf durumuna **bağımlı olmayan** yardımcı fonksiyonlardır.

```
Normal Method    → self alır  → instance state'e erişir
Class Method     → cls alır   → class state'e erişir
Static Method    → hiçbiri    → bağımsız utility fonksiyon
```

### Örnek
```python
class MathOperations:
    @staticmethod
    def add(x, y):
        return x + y

# Instance oluşturmadan çağrılabilir:
print(MathOperations.add(1, 2))   # 3
```

---

## 4. Class Method

### Kavram
`@classmethod`, ilk parametre olarak **sınıfın kendisini** (`cls`) alır. En yaygın kullanımı **alternatif constructor** (named constructor) örüntüsüdür.

### Kullanım Alanları
1. **Alternatif constructor:** Farklı parametrelerle nesne oluşturma
2. **Sınıf değişkeni yönetimi:** Sınıf düzeyindeki sayaçlara erişim

### Örnek
```python
class Pizza:
    total_pizzas = 0

    def __init__(self, ingredients):
        self.ingredients = ingredients
        Pizza.total_pizzas += 1

    @classmethod
    def margherita(cls):
        return cls(["peynir", "domates", "fesleğen"])   # cls = Pizza

    @classmethod
    def pepperoni(cls):
        return cls(["peynir", "sucuk", "domates"])

    @classmethod
    def get_total_pizzas(cls):
        return cls.total_pizzas

pizza1 = Pizza.margherita()
pizza2 = Pizza.pepperoni()
print(Pizza.get_total_pizzas())   # 2
```

> 💡 `cls(...)` yerine `Pizza(...)` da yazılabilir; ancak `cls` kullanmak, miras alındığında alt sınıfların doğru şekilde çalışmasını sağlar.

---

## 5. Abstract Methods

### Kavram
`ABC` (Abstract Base Class) ile oluşturulan sınıflardan **doğrudan instance alınamaz**. `@abstractmethod` ile işaretlenen metodlar, her alt sınıfın kendi implementasyonunu yazmak zorunda olduğu bir **sözleşme (contract)** oluşturur.

### Amaç
- Ortak arayüz (interface) tanımlamak
- Polimorfizmi garantilemek
- Eksik implementasyonu derleme zamanında (import anında) yakalamak

### Örnek
```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def make_sound(self): pass

    @abstractmethod
    def move(self): pass

class Dog(Animal):
    def make_sound(self):
        print("Hav hav!")

    def move(self):
        print("Köpek koştu.")

# Animal()     → TypeError: Can't instantiate abstract class
barley = Dog("Barley")   # ✓
barley.move()
```

---

## 6. Overloading

### Kavram
Python'da C++/Java gibi gerçek method overloading yoktur. `@overload` dekoratörü yalnızca **tip denetleyicilerine (mypy, pyright)** birden fazla imza olduğunu bildirir. Asıl çalışma mantığı tek bir implementasyon metodunda yazılır.

### Örnek
```python
from typing import overload, Union

class Calculator:
    @overload
    def add(self, a: int, b: int) -> int: ...

    @overload
    def add(self, a: int, b: int, c: int) -> int: ...

    def add(self, a: int, b: int, c: int | None = None) -> int:
        if c is None:
            return a + b
        return a + b + c

    def process(self, value: Union[int, str]) -> Union[int, str]:
        if isinstance(value, int):
            return value * 2
        elif isinstance(value, str):
            return value.upper()
```

> ⚠️ **Sık Yapılan Hata:** `@overload` metodlarında gerçek gövde yazmak. Bu metodlar sadece `...` veya `pass` içermelidir; asıl mantık imzasız (dekoratörsüz) metodda yer alır.
>
> ⚠️ **Ek Hata:** İmzasız implementasyon metodunun adını tutarsız yazmak (`proceess` vs `process`). Böyle bir durumda metod hiçbir zaman çağrılamaz.

---

## 7. Final

### Kavram
`@final` iki farklı amaçla kullanılır:

| Kullanım | Anlamı |
|---|---|
| `@final` metod | Alt sınıflar bu metodu override edemez |
| `@final` sınıf | Bu sınıftan miras alınamaz |

> ⚠️ Python runtime `@final`'ı **zorla engellemez**. Bu bir tip denetleyicisi (`mypy`, `pyright`) konvansiyonudur; ihlaller IDE veya CI'da uyarı olarak görünür.

### Örnek
```python
from typing import final

class BaseGame:
    @final
    def calculate_score(self, points: int) -> int:
        return points * 100   # Alt sınıflar bunu değiştiremez

@final
class SecretAlgorithm:
    pass   # Bu sınıftan miras alınamaz
```

> ⚠️ **Sık Yapılan Hata:** `@final` ile işaretlenmiş metodu alt sınıfta override etmek. Tip denetleyicisi uyarı verir, ancak Python çalışmaya devam eder — bu sessiz hataya yol açar.

---

## 8. Override

### Kavram
`@override` (Python 3.12+), bir metodun **gerçekten üst sınıfta var olan** bir metodu override ettiğini açıkça bildirir. Yanlış yazılmış metod adlarını (typo) erken yakalar.

### Örnek
```python
from typing import override

class Shape:
    def area(self) -> float:
        return 0.0

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    @override
    def area(self) -> float:         # ✓ Shape.area var
        return self.width * self.height

    @override
    def perimeter(self) -> float:    # ✓ Shape.perimeter var
        return 2 * (self.width + self.height)
```

> ⚠️ **Kritik Hata:** Metodları `__init__` bloğunun içine girintilendirmek. Fazla girintileme metodu yerel fonksiyon yapar — sınıf metodu değil!
>
> ```python
> # YANLIŞ ❌
> class Rectangle(Shape):
>     def __init__(self, width, height):
>         self.width = width
>         self.height = height
>         def area(self):          # Bu bir yerel fonksiyon!
>             return self.width * self.height
>
> # DOĞRU ✓
> class Rectangle(Shape):
>     def __init__(self, width, height):
>         self.width = width
>         self.height = height
>
>     def area(self):              # Bu bir sınıf metodu
>         return self.width * self.height
> ```

---

## 9. Combining Decorators

### Kavram
Birden fazla dekoratör üst üste uygulanabilir. Uygulama sırası **içten dışa** (en alttaki önce), çalışma sırası ise **dıştan içe** (en üstteki önce) şeklindedir.

```
@A
@B
def f(): ...
# f = A(B(f)) olarak okunur
```

### Örnek
```python
def multiply_decorator(func):
    def wrapper(x: int):
        return func(x) * 2
    return wrapper   # ← wrapper döndürülür

def other_decorator(func):
    def wrapper(x: int):
        return func(x) * 4
    return wrapper

@multiply_decorator   # 2. uygulanan
@other_decorator      # 1. uygulanan
def calculate(x: int):
    return x * 2

print(calculate(10))
# Adımlar: 10*2=20 → *4=80 → *2=160
```

> ⚠️ **Kritik Hata:** `return wrapper` satırını `wrapper()` fonksiyonunun **içine** yazmak. Bu durumda dış fonksiyon hiçbir şey döndürmez (`None`) ve dekoratör zincirleme tamamen bozulur.

---

## 🐛 Düzeltilen Hatalar

| # | Bölüm | Hata | Düzeltme |
|---|---|---|---|
| 1 | Section 1 | `return wrapper` yanlış girintilenmişti (fonksiyon içindeydi) | Dışarı çıkarıldı |
| 2 | Section 2 | `raise print("mesaj")` — `print` `None` döndürür | `raise ValueError("mesaj")` yapıldı |
| 3 | Section 2 | `@age.setter` içinde `self.__age = value` eksikti | Satır eklendi |
| 4 | Section 6 | `proceess` adlı metod — `process` ile uyumsuzluk | `process` olarak düzeltildi |
| 5 | Section 7 | `MyGame.calculate_score` `@final` metodu override ediyordu | Override kaldırıldı |
| 6 | Section 8 | `area()` ve `perimeter()` `__init__` içine girintilenmişti | Sınıf seviyesine taşındı |
| 7 | Section 8 | `Shape` metodlarında `@override` kullanımı (hiç miras yok) | `@override` kaldırıldı |
| 9 | Section 9 | `return wrapper` `wrapper()` içinde — dış fonksiyon `None` dönüyordu | Doğru girintiye taşındı |

---

## 🔧 Gereksinimler

```bash
Python 3.12+   # @override için
typing         # overload, Union, final, override
abc            # ABC, abstractmethod
```

---

## 📚 Kaynaklar

- [Python Docs — Decorators](https://docs.python.org/3/glossary.html#term-decorator)
- [Python Docs — abc module](https://docs.python.org/3/library/abc.html)
- [PEP 3119 — Abstract Base Classes](https://peps.python.org/pep-3119/)
- [PEP 673 — Self Type](https://peps.python.org/pep-0673/)
- [mypy — @final and @override](https://mypy.readthedocs.io/en/stable/final_attrs.html)
