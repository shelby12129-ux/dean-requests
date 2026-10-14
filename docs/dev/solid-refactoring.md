# SOLID-рефакторинг

Дата: 12.10.2026
Автор: Ишанов Афроз.

## Что такое рефакторинг

Рефакторинг — изменение внутренней структуры кода без изменения
поведения. Безопасен под защитой тестов.

## Нарушение 1: SRP (Single Responsibility Principle)

### До

Метод `report()` делал три вещи одновременно: считал сумму,
печатал результат и отправлял письмо.

def report(data):
    total = sum(data)
    print(total)
    mail(total)

**Проблема:** три причины меняться в одном методе.
Невозможно протестировать расчёт без email.

### После

Разбили на три функции — каждая с одной ответственностью.

def total(data):
    return sum(data)


def render(total):
    return f"Итого: {total}"


def send(text):
    print(f"[email] {text}")

**Что стало лучше:**
- total(data) тестируется изолированно.
- render() меняется независимо от send().
- Каждая функция — одна причина меняться.

---

## Нарушение 2: OCP (Open/Closed Principle)

### До

Функция calculate_discount() использовала if/elif по типу клиента.
При добавлении нового типа нужно менять функцию — нарушение OCP.

def calculate_discount(client_type, amount):
    if client_type == "student":
        return amount * 0.05
    elif client_type == "employee":
        return amount * 0.10
    elif client_type == "vip":
        return amount * 0.20
    return 0

**Проблема:** каждое добавление типа клиента — правка существующего кода.

### После

Применили паттерн «Стратегия» — см. app/strategy.py.

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float: ...


class StudentDiscount(DiscountStrategy):
    def calculate(self, amount): return amount * 0.05


class EmployeeDiscount(DiscountStrategy):
    def calculate(self, amount): return amount * 0.10

**Что стало лучше:**
- Новый тип = новый класс, старая логика не меняется.
- Каждая стратегия тестируется отдельно.
- Код открыт для расширения, закрыт для изменения.

---

## Что дал рефакторинг

| Показатель | До | После |
|-----------|-----|-------|
| Причин меняться в одной функции | 3 | 1 |
| Тестируемость | Низкая | Высокая |
| Добавление нового типа клиента | Правка if/elif | Новый класс |

## Связь с кодом

- SRP-рефакторинг применён в app/notifications.py.
- OCP-рефакторинг применён в app/strategy.py.
