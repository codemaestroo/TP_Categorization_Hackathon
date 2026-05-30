from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


# названия папок, куда складываем письма
class Category(str, Enum):
    INCIDENTS = "incidents"
    MONITORING = "monitoring"
    ACCESS = "access"
    SOFTWARE = "software"
    GENERAL = "general"
    SPAM = "spam"
    UNCLASSIFIED = "unclassified"
    FAILED = "failed"


@dataclass
class Email:
    source_path: Path
    sender: str
    subject: str
    body: str
    raw_format: str  # txt, json или no_ext


@dataclass
class ClassificationResult:
    category: Category
    reason: str


@dataclass
class ProcessingStats:
    total: int = 0
    by_category: dict[str, int] = field(default_factory=dict)
    failed: int = 0

    def add(self, category: Category):
        self.total += 1
        name = category.value
        if name not in self.by_category:
            self.by_category[name] = 0
        self.by_category[name] += 1
        if category == Category.FAILED:
            self.failed += 1

    def report_lines(self):
        lines = [f"Всего обработано: {self.total}"]
        for name, count in sorted(self.by_category.items()):
            lines.append(f"{name}: {count}")
        return lines
