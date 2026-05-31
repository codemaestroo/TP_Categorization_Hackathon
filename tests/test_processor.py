from mail_system.processor import MailProcessor
from mail_system.storage import copy_inbox_files, ensure_mailbox_layout


def test_processor_moves_files(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "urgent.txt").write_text(
        "From: a@b\nSubject: URGENT: fail\n\nHelp\n",
        encoding="utf-8",
    )
    (source / "bad.bin").write_bytes(b"\x01\x02")

    mailbox = tmp_path / "mailbox"
    ensure_mailbox_layout(mailbox)
    copy_inbox_files(source, mailbox / "inbox")

    stats = MailProcessor(mailbox).run()

    assert stats.total == 2
    assert stats.failed == 1
    assert (mailbox / "incidents" / "urgent.txt").exists()
    assert (mailbox / "failed" / "bad.bin").exists()
    assert (mailbox / "stats.txt").exists()
    assert (mailbox / "processing.log").exists()
