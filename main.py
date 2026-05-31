import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mail_system.processor import MailProcessor
from mail_system.storage import (
    copy_inbox_files,
    ensure_mailbox_layout,
    extract_zip,
    inbox_is_empty,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Сортировка входящих писем по категориям",
    )
    parser.add_argument(
        "--mailbox",
        default="mailbox",
        help="папка для inbox, категорий и логов",
    )
    parser.add_argument(
        "--source",
        default="data/inbox/inbox",
        help="откуда брать письма, если inbox пустой",
    )
    parser.add_argument(
        "--zip",
        default="",
        help="путь к zip (необязательно)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="очистить inbox и скопировать письма заново",
    )
    return parser


def prepare_inbox(mailbox_root: Path, source_dir: Path, zip_path: Path | None, force: bool) -> None:
    ensure_mailbox_layout(mailbox_root)
    inbox_dir = mailbox_root / "inbox"

    if force and inbox_dir.exists():
        for path in inbox_dir.iterdir():
            if path.is_file():
                path.unlink()

    if zip_path and zip_path.exists():
        extract_zip(zip_path, mailbox_root)
        return

    if inbox_is_empty(inbox_dir) and source_dir.exists():
        copy_inbox_files(source_dir, inbox_dir)


def main() -> int:
    args = build_parser().parse_args()
    mailbox_root = Path(args.mailbox)
    source_dir = Path(args.source)
    zip_path = Path(args.zip) if args.zip else None

    if not source_dir.exists() and not (zip_path and zip_path.exists()):
        print(f"Ошибка: не найден источник писем ({source_dir})", file=sys.stderr)
        return 1

    prepare_inbox(mailbox_root, source_dir, zip_path, args.force)

    processor = MailProcessor(mailbox_root)
    stats = processor.run()

    print(f"OK: обработано {stats.total}, ошибок {stats.failed}")
    print(f"Лог: {processor.log_path}")
    print(f"Статистика: {processor.stats_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
