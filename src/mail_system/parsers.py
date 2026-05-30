import json
import re
from pathlib import Path

from .models import Email


class ParseError(Exception):
    """Не смогли прочитать файл как письмо."""


# расширения, которые точно не текст
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

    for encoding in ("utf-8", "cp1251", "latin-1"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue

    raise ParseError("не удалось определить кодировку")


def parse_text_content(text: str, path: Path, raw_format: str) -> Email:
    sender = ""
    subject = ""
    body_lines = []
    in_body = False

    for line in text.splitlines():
        if not in_body:
            if line.strip() == "":
                in_body = True
                continue

            from_match = re.match(r"^(?:From|От(?: кого)?)\s*:\s*(.*)$", line, re.IGNORECASE)
            if from_match:
                sender = from_match.group(1).strip()
                continue

            subject_match = re.match(r"^(?:Subject|Тема)\s*:\s*(.*)$", line, re.IGNORECASE)
            if subject_match:
                subject = subject_match.group(1).strip()
                continue

            # To, Date и т.п. просто пропускаем
            if re.match(r"^(?:To|Кому|Date|Дата)\s*:", line, re.IGNORECASE):
                continue
        else:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()
    return Email(
        source_path=path,
        sender=sender,
        subject=subject,
        body=body,
        raw_format=raw_format,
    )


def parse_json_content(text: str, path: Path) -> Email:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as err:
        raise ParseError(f"битый json: {err}") from err

    if not isinstance(data, dict):
        raise ParseError("json должен быть объектом")

    body = data.get("body", "")
    if body is None:
        body = ""
    if not isinstance(body, str):
        body = str(body)

    return Email(
        source_path=path,
        sender=str(data.get("from", "")),
        subject=str(data.get("subject", "")),
        body=body,
        raw_format="json",
    )


class EmailParser:
    def parse(self, path: Path) -> Email:
        path = Path(path)

        if should_skip_file(path):
            raise ParseError("служебный файл, пропускаем")

        suffix = path.suffix.lower()

        if suffix in BINARY_EXTENSIONS:
            raise ParseError(f"бинарный формат {suffix}")

        text = read_text(path)

        if suffix == ".json":
            return parse_json_content(text, path)

        # .txt и файлы без расширения читаем одинаково
        if suffix in ("", ".txt"):
            fmt = "no_ext" if suffix == "" else "txt"
            return parse_text_content(text, path, fmt)

        raise ParseError(f"неизвестный формат {suffix}")
