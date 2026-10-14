"""Тесты модуля работы с заявками."""

import pytest

from app.requests import RequestService, RequestStatus


@pytest.fixture
def service():
    """Свежий сервис для каждого теста."""
    return RequestService()


class TestRegister:
    """Тесты регистрации заявок."""

    def test_register_valid(self, service):
        """Валидная заявка создаётся."""
        request = service.register("Иванов И.И.", "Нужна справка")
        assert request.request_id == 1
        assert request.student_name == "Иванов И.И."
        assert request.status == RequestStatus.NEW

    def test_register_assigns_incrementing_ids(self, service):
        """Номера заявок увеличиваются."""
        r1 = service.register("Иванов", "Заявка 1")
        r2 = service.register("Петров", "Заявка 2")
        assert r1.request_id == 1
        assert r2.request_id == 2

    def test_register_empty_name(self, service):
        """Пустое имя — ValueError."""
        with pytest.raises(ValueError):
            service.register("", "Описание")

    def test_register_empty_description(self, service):
        """Пустое описание — ValueError."""
        with pytest.raises(ValueError):
            service.register("Иванов", "")

    def test_register_long_name(self, service):
        """Граница: длинное имя (100 символов)."""
        long_name = "А" * 100
        request = service.register(long_name, "Описание")
        assert request.student_name == long_name


class TestFind:
    """Тесты поиска заявок."""

    def test_find_by_student(self, service):
        """Поиск по имени студента работает."""
        service.register("Иванов", "Заявка 1")
        service.register("Петров", "Заявка 2")
        service.register("Иванов", "Заявка 3")

        found = service.find_by_student("Иванов")
        assert len(found) == 2

    def test_find_by_student_no_matches(self, service):
        """Поиск без совпадений возвращает пустой список."""
        service.register("Иванов", "Заявка")
        found = service.find_by_student("Сидоров")
        assert found == []


class TestAssignExecutor:
    """Тесты назначения исполнителя."""

    def test_assign_to_new_request(self, service):
        """Назначение на новую заявку работает."""
        service.register("Иванов", "Описание")
        request = service.assign_executor(1, "Смирнова")
        assert request.status == RequestStatus.IN_PROGRESS
        assert request.executor == "Смирнова"

    def test_assign_to_in_progress(self, service):
        """Нельзя назначить на заявку в работе."""
        service.register("Иванов", "Описание")
        service.assign_executor(1, "Смирнова")
        with pytest.raises(ValueError):
            service.assign_executor(1, "Кузнецов")

    def test_assign_unknown_id(self, service):
        """Несуществующий ID — ValueError."""
        with pytest.raises(ValueError):
            service.assign_executor(999, "Смирнова")


class TestClose:
    """Тесты закрытия заявок."""

    def test_close_done_request(self, service):
        """Закрытие выполненной заявки работает."""
        service.register("Иванов", "Описание")
        service.assign_executor(1, "Смирнова")

        # Вручную переводим в DONE (в реальной системе — отдельный метод)
        request = service._find(1)
        request.status = RequestStatus.DONE

        closed = service.close(1)
        assert closed.status == RequestStatus.CLOSED

    def test_close_new_request(self, service):
        """Нельзя закрыть новую заявку."""
        service.register("Иванов", "Описание")
        with pytest.raises(ValueError):
            service.close(1)

    def test_close_unknown_id(self, service):
        """Несуществующий ID — ValueError."""
        with pytest.raises(ValueError):
            service.close(999)
