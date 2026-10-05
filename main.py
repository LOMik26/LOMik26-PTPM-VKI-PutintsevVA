import logging
import sys
from pathlib import Path

from registration_validator import mask_password, validate_registration


def configure_logger():
    log_dir = Path(__file__).resolve().parent / "Logs"
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger("registration")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s | [%(levelname)-7s] | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_dir / "registration.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


def main():
    logger = configure_logger()

    try:
        logger.info("Приложение запущено")

        if len(sys.argv) > 1:
            args = sys.argv[1:]
            if len(args) >= 3:
                login, password, confirmation = args[:3]
            else:
                login = input("Введите логин: ")
                password = input("Введите пароль: ")
                confirmation = input("Подтвердите пароль: ")
        else:
            login = input("Введите логин: ")
            password = input("Введите пароль: ")
            confirmation = input("Подтвердите пароль: ")

        login = login.lstrip("\ufeff").strip()
        password = password.lstrip("\ufeff")
        confirmation = confirmation.lstrip("\ufeff")

        logger.info(
            "Входные данные: login=%s, password=%s, confirm=%s",
            login,
            mask_password(password),
            mask_password(confirmation),
        )

        is_valid, message = validate_registration(login, password, confirmation)
        logger.info("Результат проверки: %s | %s", is_valid, message or "успешно")

        print(is_valid)
        print(message)

        if is_valid:
            logger.info("Регистрация успешно завершена.")
        else:
            logger.warning("Регистрация завершилась с ошибками: %s", message)

    except Exception:
        logger.exception("Ошибка при выполнении программы")
        print(False)
        print("Произошла непредвиденная ошибка.")
        raise


if __name__ == "__main__":
    main()
