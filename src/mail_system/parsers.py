import json
import re
from pathlib import Path

from .models import Email


class ParseError(Exception): # Позже добавляем в failed
    """Не смогли прочитать файл как письмо."""


# расширения, которые точно не текст - значит не письмо - значит залетный файл или ошибка
BINARY_EXTENSIONS = {".bin", ".jpeg", ".jpg", ".png", ".gif", ".pdf"}


def should_skip_file(path: Path) -> bool:
    name = path.name
    if name == ".DS_Store":
        return True
    if name.startswith("."):
        return True
    return False


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    if not raw.strip():
        raise ParseError("файл пустой")

    for encoding in ("utf-8", "cp1251", "latin-1"): # учитываем все известные мне кодировки)
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue

    raise ParseError("не удалось определить кодировку") # -except


