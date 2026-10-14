"""Интеграционные тесты: проверка совместной работы модулей."""

from app.auth import authenticate
from app.notifications import EmailNotifier, notify_status_change
from app.requests import RequestService
from app.strategy import AssignmentContext, Executor, LeastLoadedStrategy


def test_full_request_lifecycle():
    """Полный цикл: авторизация → заявка → назначение → уведомление."""
    # 1. Авторизация сотрудника
    employee = authenticate("employee1", "pass456")
    assert employee is not None

    # 2. Регистрация заявки
    service = RequestService()
    request = service.register("Иванов И.И.", "Нужна справка")
    assert request.request_id == 1

    # 3. Подбор исполнителя через стратегию
    executors = [
        Executor(name="Смирнова", open_requests=3),
        Executor(name="Кузнецов", open_requests=1),
    ]
    context = AssignmentContext(LeastLoadedStrategy())
    chosen = context.assign(executors)
    assert chosen.name == "Кузнецов"

    # 4. Назначение
    service.assign_executor(1, chosen.name)
    assert service.get_all()[0].executor == "Кузнецов"

    # 5. Уведомление
    notifier = EmailNotifier()
    result = notify_status_change(
        notifier,
        recipient="ivanov@example.com",
        request_id=1,
        new_status="В работе",
    )
    assert result is True
    assert len(notifier.log) == 1


def test_auth_and_access_integration():
    """Связка: авторизация + проверка доступа."""
    from app.auth import has_access

    student = authenticate("student1", "pass123")
    employee = authenticate("employee1", "pass456")

    assert has_access(student, "create_request") is True
    assert has_access(student, "assign_executor") is False
    assert has_access(employee, "assign_executor") is True
