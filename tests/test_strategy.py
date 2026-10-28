"""Тесты паттерна «Стратегия» для выбора исполнителя."""

import pytest

from app.strategy import (
    AssignmentContext,
    Executor,
    LeastLoadedStrategy,
    ManualStrategy,
    RandomStrategy,
)


@pytest.fixture
def executors():
    """Набор исполнителей для тестов."""
    return [
        Executor(name="Смирнова", open_requests=5),
        Executor(name="Кузнецов", open_requests=2),
        Executor(name="Петрова", open_requests=8),
    ]


class TestLeastLoadedStrategy:
    """Тесты стратегии «наименьшая загрузка»."""

    def test_chooses_least_loaded(self, executors):
        """Выбирает исполнителя с минимальной загрузкой."""
        strategy = LeastLoadedStrategy()
        chosen = strategy.choose(executors)
        assert chosen.name == "Кузнецов"
        assert chosen.open_requests == 2

    def test_ignores_off_duty(self, executors):
        """Игнорирует исполнителей не на смене."""
        executors[1].on_duty = False  # Кузнецов недоступен
        strategy = LeastLoadedStrategy()
        chosen = strategy.choose(executors)
        assert chosen.name == "Смирнова"

    def test_returns_none_if_all_off_duty(self, executors):
        """Возвращает None, если все недоступны."""
        for e in executors:
            e.on_duty = False
        strategy = LeastLoadedStrategy()
        assert strategy.choose(executors) is None

    def test_returns_none_for_empty_list(self):
        """Возвращает None для пустого списка."""
        strategy = LeastLoadedStrategy()
        assert strategy.choose([]) is None


class TestRandomStrategy:
    """Тесты стратегии «случайный выбор»."""

    def test_returns_some_executor(self, executors):
        """Возвращает какого-то исполнителя из доступных."""
        strategy = RandomStrategy()
        chosen = strategy.choose(executors)
        assert chosen is not None
        assert chosen in executors

    def test_returns_none_if_all_off_duty(self, executors):
        """Возвращает None, если все недоступны."""
        for e in executors:
            e.on_duty = False
        strategy = RandomStrategy()
        assert strategy.choose(executors) is None


class TestManualStrategy:
    """Тесты стратегии «ручное назначение»."""

    def test_chooses_named_executor(self, executors):
        """Выбирает исполнителя по имени."""
        strategy = ManualStrategy("Петрова")
        chosen = strategy.choose(executors)
        assert chosen.name == "Петрова"

    def test_returns_none_for_unknown_name(self, executors):
        """Возвращает None, если имени нет в списке."""
        strategy = ManualStrategy("Неизвестный")
        assert strategy.choose(executors) is None

    def test_returns_none_if_off_duty(self, executors):
        """Возвращает None, если исполнитель не на смене."""
        executors[2].on_duty = False  # Петрова недоступна
        strategy = ManualStrategy("Петрова")
        assert strategy.choose(executors) is None


class TestAssignmentContext:
    """Тесты контекста стратегии."""

    def test_uses_initial_strategy(self, executors):
        """Использует стратегию, переданную при создании."""
        context = AssignmentContext(LeastLoadedStrategy())
        chosen = context.assign(executors)
        assert chosen.name == "Кузнецов"

    def test_can_switch_strategy(self, executors):
        """Можно сменить стратегию на лету."""
        context = AssignmentContext(LeastLoadedStrategy())
        context.set_strategy(ManualStrategy("Петрова"))
        chosen = context.assign(executors)
        assert chosen.name == "Петрова"
