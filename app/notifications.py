"""Модуль уведомлений.

Отправляет e-mail-уведомления студентам при смене статуса заявки.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Protocol


class Notifier(Protocol):
    """Интерфейс отправителя уведомлений."""

    def send(self, recipient: str, message: str) -> bool:
        """Отправляет уведомление получателю."""
        ...


@dataclass
class EmailNotifier:
    """Отправитель e-mail-уведомлений."""

    sender: str = "noreply@dean-requests.local"
    _log: List[str] = field(default_factory=list)

    def send(self, recipient: str, message: str) -> bool:
        """Имитирует отправку письма, сохраняя его в журнал."""
        if not recipient or not message:
            return False

        entry = (
            f"[{datetime.now():%Y-%m-%d %H:%M}] "
            f"to={recipient} from={self.sender}: {message}"
        )
        self._log.append(entry)
        print(entry)
        return True

    @property
    def log(self) -> List[str]:
        """Журнал отправленных писем."""
        return list(self._log)


def notify_status_change(
    notifier: Notifier,
    recipient: str,
    request_id: int,
    new_status: str,
) -> bool:
    """Уведомляет студента о смене статуса заявки."""
    message = f"Статус заявки №{request_id} изменён на «{new_status}»"
    return notifier.send(recipient, message)
