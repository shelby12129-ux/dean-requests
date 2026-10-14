"""Модуль авторизации пользователей."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """Пользователь системы."""
    username: str
    role: str


_USERS = {
    "student1": {"password": "pass123", "role": "student"},
    "employee1": {"password": "pass456", "role": "employee"},
    "admin1": {"password": "admin789", "role": "admin"},
}


def authenticate(username: str, password: str) -> Optional[User]:
    """Проверяет учётные данные."""
    if not username or not password:
        return None
    record = _USERS.get(username)
    if record is None or record["password"] != password:
        return None
    return User(username=username, role=record["role"])


def has_access(user: User, resource: str) -> bool:
    """Проверяет доступ пользователя к ресурсу."""
    access_rules = {
        "student": ["view_own_requests", "create_request"],
        "employee": ["view_all_requests", "assign_executor", "close_request"],
        "admin": ["manage_users", "manage_dictionaries"],
    }
    return resource in access_rules.get(user.role, [])
