import pytest
from pathlib import Path

from mail_system.models import Category, Email
from mail_system.parsers import EmailParser, ParseError
from mail_system.classifier import RuleBasedClassifier


FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def parser():
    return EmailParser()


@pytest.fixture
def classifier():
    return RuleBasedClassifier()


def test_parse_ru_headers(parser):
    email = parser.parse(FIXTURES / "urgent.txt")
    assert email.subject == "URGENT: server down"
    assert "test@company.ru" in email.sender


def test_parse_json(parser):
    email = parser.parse(FIXTURES / "valid.json")
    assert email.subject == "test"
    assert email.body == "hello"


def test_broken_json(parser):
    with pytest.raises(ParseError):
        parser.parse(FIXTURES / "broken.json")


def test_empty_file(parser, tmp_path):
    path = tmp_path / "empty.txt"
    path.write_text("", encoding="utf-8")
    with pytest.raises(ParseError):
        parser.parse(path)


def test_binary_file(parser, tmp_path):
    path = tmp_path / "bad.bin"
    path.write_bytes(b"\x00\x01\x02")
    with pytest.raises(ParseError):
        parser.parse(path)


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("urgent.txt", Category.INCIDENTS),
        ("alert.txt", Category.MONITORING),
        ("spam.txt", Category.SPAM),
    ],
)
def test_classifier_categories(classifier, parser, filename, expected):
    email = parser.parse(FIXTURES / filename)
    result = classifier.classify(email)
    assert result.category == expected


def test_unclassified(classifier):
    email = Email(
        source_path=Path("x.txt"),
        sender="a@b",
        subject="hello",
        body="just saying hi",
        raw_format="txt",
    )
    result = classifier.classify(email)
    assert result.category == Category.UNCLASSIFIED
