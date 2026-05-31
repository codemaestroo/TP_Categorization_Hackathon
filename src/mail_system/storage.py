import shutil
import zipfile
from pathlib import Path

from .models import Category


def ensure_mailbox_layout(mailbox_root: Path) -> None:
    mailbox_root.mkdir(parents=True, exist_ok=True)
    (mailbox_root / "inbox").mkdir(exist_ok=True)
    for category in Category:
        (mailbox_root / category.value).mkdir(exist_ok=True)


def unique_dest_path(dest_dir: Path, filename: str) -> Path:
    dest = dest_dir / filename
    if not dest.exists():
        return dest

    stem = dest.stem
    suffix = dest.suffix
    counter = 1
    while True:
        candidate = dest_dir / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def move_file(src: Path, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = unique_dest_path(dest_dir, src.name)
    shutil.move(str(src), str(dest))
    return dest


def extract_zip(zip_path: Path, target_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as archive:
        archive.extractall(target_dir)


def copy_inbox_files(source_dir: Path, inbox_dir: Path) -> int:
    inbox_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(source_dir.iterdir()):
        if path.is_file() and not path.name.startswith("."):
            dest = unique_dest_path(inbox_dir, path.name)
            shutil.copy2(path, dest)
            count += 1
    return count


def inbox_is_empty(inbox_dir: Path) -> bool:
    if not inbox_dir.exists():
        return True
    for path in inbox_dir.iterdir():
        if path.is_file() and not path.name.startswith("."):
            return False
    return True
