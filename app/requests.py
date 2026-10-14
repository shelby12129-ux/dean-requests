"""Модуль работы с заявками.

Отвечает за регистрацию, назначение исполнителя и закрытие заявок.
"""

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import List, Optional


class RequestStatus(Enum):
    """Статусы заявки."""
    NEW = "Новая"
    IN_PROGRESS = "В работе"
    DONE = "Выполнена"
    CLOSED = "Закрыта"
    CANCELLED = "Отменена"


@dataclass
class Request:
    """Заявка студента."""
    request_id: int
    student_name: str
    description: str
    status: RequestStatus = RequestStatus.NEW
    created_at: date = field(default_factory=date.today)
    executor: Optional[str] = None


class RequestService:
    """Сервис управления заявками."""

    def __init__(self) -> None:
        self._requests: List[Request] = []
        self._next_id = 1

    def register(self, student_name: str, description: str) -> Request:
        """Регистрирует новую заявку."""
        if not student_name or not description:
            raise ValueError("Имя студента и описание обязательны")

        request = Request(
            request_id=self._next_id,
            student_name=student_name,
            description=description,
        )
        self._requests.append(request)
        self._next_id += 1
        return request

    def get_all(self) -> List[Request]:
        """Возвращает все заявки."""
        return list(self._requests)

    def find_by_student(self, student_name: str) -> List[Request]:
        """Ищет заявки по имени студента."""
        return [r for r in self._requests if r.student_name == student_name]

    def assign_executor(self, request_id: int, executor: str) -> Request:
        """Назначает исполнителя на заявку."""
        request = self._find(request_id)
        if request.status != RequestStatus.NEW:
            raise ValueError("Назначить можно только новую заявку")
        request.executor = executor
        request.status = RequestStatus.IN_PROGRESS
        return request

    def close(self, request_id: int) -> Request:
        """Закрывает заявку."""
        request = self._find(request_id)
        if request.status != RequestStatus.DONE:
            raise ValueError("Закрыть можно только выполненную заявку")
        request.status = RequestStatus.CLOSED
        return request

    def _find(self, request_id: int) -> Request:
        for r in self._requests:
            if r.request_id == request_id:
                return r
        raise ValueError(f"Заявка с номером {request_id} не найдена")
