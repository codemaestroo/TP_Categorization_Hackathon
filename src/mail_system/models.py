from dataclasses import dataclass, field #библиотека для классов контейнеров
from enum import Enum # набор констант (наших)
from pathlib import Path


# названия папок, куда складываем письма
class Category(str, Enum): # через Enum фиксацию
    INCIDENTS = "incidents"
    MONITORING = "monitoring"
    ACCESS = "access"
    SOFTWARE = "software"
    GENERAL = "general"
    SPAM = "spam"
    UNCLASSIFIED = "unclassified"
    FAILED = "failed" # надо придумать что с этим делать


#тута поправить потом, черновой вариант классов
@dataclass
class Email:
    source_path: Path
    sender: str
    subject: str
    body: str
    raw_format: str  # txt, json


# Определили класс - определилил категорию
@dataclass
class ClassificationResult:
    category: Category
    reason: str #формат вывода причины в лог: причина есть - текст, нет - пустой текст(плохо)


@dataclass
class ProcessingStats:
    total: int = 0
    by_category: dict[str, int] = field(default_factory=dict)
    failed: int = 0 # если траблы

    def add(self, category: Category):
        self.total += 1
        name = category.value
        if name not in self.by_category:
            self.by_category[name] = 0
        self.by_category[name] += 1
        if category == Category.FAILED:
            self.failed += 1


    # сбор логов на будущее
    def report_lines(self):
        lines = [f"Всего обработано: {self.total}"]
        for name, count in sorted(self.by_category.items()):
            lines.append(f"{name}: {count}")
        return lines
