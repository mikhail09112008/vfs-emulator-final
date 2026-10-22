"""Парсер командной строки с поддержкой кавычек."""
import shlex


def parse(line: str) -> list[str]:
    """Разбирает строку на токены. Поддерживает '...' и \"...\"."""
    try:
        return shlex.split(line)
    except ValueError as e:
        raise ValueError(f"Ошибка разбора строки: {e}") from e