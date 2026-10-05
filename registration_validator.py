import hashlib
import re

BLACKLIST = {
    "admin",
    "administrator",
    "guest",
    "manager",
    "root",
    "superuser",
    "support",
    "testuser",
    "user",
    "users",
    "login",
    "password",
    "qwerty",
    "default",
}

PHONE_RE = re.compile(r"^\+\d-\d{3}-\d{3}-\d{4}$")
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")
USERNAME_RE = re.compile(r"^[A-Za-z0-9_]+$")
UPPER_CYRILLIC_RE = re.compile(r"[А-ЯЁ]")
LOWER_CYRILLIC_RE = re.compile(r"[а-яё]")
DIGIT_RE = re.compile(r"\d")
SPECIAL_RE = re.compile(r"[^А-Яа-яЁё0-9\s]")
PASSWORD_CHAR_RE = re.compile(r"^[А-Яа-яЁё0-9!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~]+$")


def mask_password(password: str) -> str:
    """Return a deterministic masked representation for logging."""
    if password is None:
        return "<empty>"
    return hashlib.sha256(password.encode("utf-8")).hexdigest()[:32]


def validate_registration(login: str, password: str, confirm_password: str):
    issues = []

    login = "" if login is None else str(login).lstrip("\ufeff").strip()
    password = "" if password is None else str(password).lstrip("\ufeff")
    confirm_password = "" if confirm_password is None else str(confirm_password).lstrip("\ufeff")

    if not login:
        issues.append("Логин не может быть пустым.")
    elif PHONE_RE.fullmatch(login) or EMAIL_RE.fullmatch(login):
        pass
    else:
        if len(login) < 5:
            issues.append("Логин должен содержать минимум 5 символов.")
        if not USERNAME_RE.fullmatch(login):
            issues.append("Логин должен содержать только латиницу, цифры и знак подчеркивания _.")
        if login.lower() in BLACKLIST:
            issues.append("Логин запрещен черным списком.")

    if not password:
        issues.append("Пароль не может быть пустым.")
    else:
        if len(password) < 7:
            issues.append("Пароль должен содержать минимум 7 символов.")
        if not PASSWORD_CHAR_RE.fullmatch(password):
            issues.append("Пароль должен содержать только кириллицу, цифры и спецсимволы.")
        if not UPPER_CYRILLIC_RE.search(password):
            issues.append("Пароль должен содержать хотя бы одну букву верхнего регистра.")
        if not LOWER_CYRILLIC_RE.search(password):
            issues.append("Пароль должен содержать хотя бы одну букву нижнего регистра.")
        if not DIGIT_RE.search(password):
            issues.append("Пароль должен содержать хотя бы одну цифру.")
        if not SPECIAL_RE.search(password):
            issues.append("Пароль должен содержать хотя бы один спецсимвол.")

    if password != confirm_password:
        issues.append("Пароль и подтверждение пароля не совпадают.")

    unique_issues = []
    seen = set()
    for issue in issues:
        if issue not in seen:
            seen.add(issue)
            unique_issues.append(issue)

    return (len(unique_issues) == 0), "; ".join(unique_issues)
