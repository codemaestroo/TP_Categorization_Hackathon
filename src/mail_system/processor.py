from pathlib import Path

from .classifier import RuleBasedClassifier
from .logging_setup import setup_logger
from .models import Category, ProcessingStats
from .parsers import EmailParser, ParseError
from .storage import move_file


class MailProcessor:
    def __init__(self, mailbox_root: Path):
        self.mailbox_root = Path(mailbox_root)
        self.inbox_dir = self.mailbox_root / "inbox"
        self.log_path = self.mailbox_root / "processing.log"
        self.stats_path = self.mailbox_root / "stats.txt"
        self.parser = EmailParser()
        self.classifier = RuleBasedClassifier()
        self.logger = setup_logger(self.log_path)

    def run(self) -> ProcessingStats:
        stats = ProcessingStats()
        files = [
            path
            for path in sorted(self.inbox_dir.iterdir())
            if path.is_file() and not path.name.startswith(".")
        ]

        for path in files:
            try:
                email = self.parser.parse(path)
                result = self.classifier.classify(email)
                dest_dir = self.mailbox_root / result.category.value
                move_file(path, dest_dir)
                stats.add(result.category)
                self.logger.info(
                    "%s -> %s | %s",
                    path.name,
                    result.category.value,
                    result.reason,
                )
            except ParseError as err:
                dest_dir = self.mailbox_root / Category.FAILED.value
                if path.exists():
                    move_file(path, dest_dir)
                stats.add(Category.FAILED)
                self.logger.error("%s -> failed | %s", path.name, err)

        self._write_stats(stats)
        return stats

    def _write_stats(self, stats: ProcessingStats) -> None:
        lines = stats.report_lines()
        self.stats_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
