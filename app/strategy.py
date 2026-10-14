"""Паттерн «Стратегия» для выбора исполнителя заявки.

Обоснование выбора паттерна:
в системе есть несколько способов назначить исполнителя
(по загрузке, случайно, вручную). Поведение варьируется,
но интерфейс один — классический случай для «Стратегии».
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Executor:
    """Исполнитель заявки."""
    name: str
    open_requests: int = 0
    on_duty: bool = True


class AssignmentStrategy(ABC):
    """Абстрактная стратегия выбора исполнителя."""

    @abstractmethod
    def choose(self, executors: List[Executor]) -> Optional[Executor]:
        """Возвращает выбранного исполнителя или None."""
        ...


class LeastLoadedStrategy(AssignmentStrategy):
    """Выбирает исполнителя с наименьшей загрузкой.

    Основная стратегия системы. Реализует ФТ-2.
    """

    def choose(self, executors: List[Executor]) -> Optional[Executor]:
        available = [e for e in executors if e.on_duty]
        if not available:
            return None
        return min(available, key=lambda e: e.open_requests)


class RandomStrategy(AssignmentStrategy):
    """Выбирает случайного исполнителя из свободных.

    Используется как альтернатива для тестов или равномерной нагрузки.
    """

    def choose(self, executors: List[Executor]) -> Optional[Executor]:
        import random
        available = [e for e in executors if e.on_duty]
        if not available:
            return None
        return random.choice(available)


class ManualStrategy(AssignmentStrategy):
    """Исполнитель назначается вручную.

    Стратегия-заглушка для случаев, когда диспетчер выбирает сам.
    """

    def __init__(self, executor_name: str) -> None:
        self.executor_name = executor_name

    def choose(self, executors: List[Executor]) -> Optional[Executor]:
        for e in executors:
            if e.name == self.executor_name and e.on_duty:
                return e
        return None


class AssignmentContext:
    """Контекст, использующий стратегию."""

    def __init__(self, strategy: AssignmentStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: AssignmentStrategy) -> None:
        """Меняет стратегию на лету."""
        self._strategy = strategy

    def assign(self, executors: List[Executor]) -> Optional[Executor]:
        """Выбирает исполнителя текущей стратегией."""
        return self._strategy.choose(executors)
