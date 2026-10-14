"""Тесты модуля авторизации."""

import pytest

from app.auth import authenticate, has_access


class TestAuthenticate:
    """Тесты функции authenticate()."""

    def test_valid_student(self):
        """Валидный студент входит успешно."""
        user = authenticate("student1", "pass123")
        assert user is not None
        assert user.username == "student1"
        assert user.role == "student"

    def test_valid_employee(self):
        """Валидный сотрудник входит успешно."""
        user = authenticate("employee1", "pass456")
        assert user is not None
        assert user.role == "employee"

    def test_valid_admin(self):
        """Валидный админ входит успешно."""
        user = authenticate("admin1", "admin789")
        assert user is not None
        assert user.role == "admin"

    def test_unknown_user(self):
        """Несуществующий логин — None."""
        assert authenticate("unknown", "pass123") is None

    def test_wrong_password(self):
        """Неверный пароль — None."""
        assert authenticate("student1", "wrong") is None

    def test_empty_username(self):
        """Пустой логин — None."""
        assert authenticate("", "pass123") is None

    def test_empty_password(self):
        """Пустой пароль — None."""
        assert authenticate("student1", "") is None

    def test_none_username(self):
        """None вместо логина — None."""
        assert authenticate(None, "pass123") is None


class TestHasAccess:
    """Тесты функции has_access()."""

    def test_student_can_create_request(self):
        """Студент может создавать заявки."""
        user = authenticate("student1", "pass123")
        assert has_access(user, "create_request") is True

    def test_student_cannot_manage_users(self):
        """Студент не может управлять пользователями."""
        user = authenticate("student1", "pass123")
        assert has_access(user, "manage_users") is False

    def test_employee_can_assign(self):
        """Сотрудник может назначать исполнителя."""
        user = authenticate("employee1", "pass456")
        assert has_access(user, "assign_executor") is True

    def test_admin_can_manage_users(self):
        """Админ может управлять пользователями."""
        user = authenticate("admin1", "admin789")
        assert has_access(user, "manage_users") is True
