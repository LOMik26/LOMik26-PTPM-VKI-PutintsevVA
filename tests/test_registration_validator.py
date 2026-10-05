import unittest

from registration_validator import validate_registration


class TestRegistrationValidator(unittest.TestCase):
    def test_valid_email_is_accepted(self):
        valid, message = validate_registration("user@example.com", "Пароль1!", "Пароль1!")
        self.assertTrue(valid)
        self.assertEqual(message, "")

    def test_valid_phone_is_accepted(self):
        valid, message = validate_registration("+7-999-123-4567", "Пароль1!", "Пароль1!")
        self.assertTrue(valid)
        self.assertEqual(message, "")

    def test_valid_plain_username_is_accepted(self):
        valid, message = validate_registration("user_42", "Пароль1!", "Пароль1!")
        self.assertTrue(valid)
        self.assertEqual(message, "")

    def test_empty_login_is_rejected(self):
        valid, message = validate_registration("", "Пароль1!", "Пароль1!")
        self.assertFalse(valid)
        self.assertIn("Логин не может быть пустым", message)

    def test_short_login_is_rejected(self):
        valid, message = validate_registration("abc", "Пароль1!", "Пароль1!")
        self.assertFalse(valid)
        self.assertIn("Логин должен содержать минимум 5 символов", message)

    def test_username_with_invalid_symbols_is_rejected(self):
        valid, message = validate_registration("user-name", "Пароль1!", "Пароль1!")
        self.assertFalse(valid)
        self.assertIn("только латиницу, цифры и знак подчеркивания", message)

    def test_blacklisted_login_is_rejected(self):
        valid, message = validate_registration("admin", "Пароль1!", "Пароль1!")
        self.assertFalse(valid)
        self.assertIn("черным списком", message)

    def test_valid_password_with_cyrillic_digits_and_special_is_accepted(self):
        valid, message = validate_registration("user_name", "СильныйПароль1!", "СильныйПароль1!")
        self.assertTrue(valid)
        self.assertEqual(message, "")

    def test_password_without_uppercase_is_rejected(self):
        valid, message = validate_registration("user_name", "сильныйпароль1!", "сильныйпароль1!")
        self.assertFalse(valid)
        self.assertIn("верхнего регистра", message)

    def test_password_without_special_symbol_is_rejected(self):
        valid, message = validate_registration("user_name", "СильныйПароль1", "СильныйПароль1")
        self.assertFalse(valid)
        self.assertIn("спецсимвол", message)

    def test_password_mismatch_is_rejected(self):
        valid, message = validate_registration("user_name", "СильныйПароль1!", "СильныйПароль2!")
        self.assertFalse(valid)
        self.assertIn("не совпадают", message)


if __name__ == "__main__":
    unittest.main()
