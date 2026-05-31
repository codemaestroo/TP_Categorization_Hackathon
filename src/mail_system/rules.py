import re

from .models import Category


class Rule:
    def __init__(self, category, pattern, reason):
        self.category = category
        self.pattern = re.compile(pattern, re.IGNORECASE)
        self.reason = reason


# порядок важен: сверху вниз
RULES = [
    Rule(
        Category.SPAM,
        r"выиграл|iphone\s*15|password-reset|лотере|крипт|заблокирован|"
        r"corp-password|click here|бесплатн",
        "похоже на спам или фишинг",
    ),
    Rule(
        Category.MONITORING,
        r"ALERT:|healthcheck|grafana|jira\.internal|monitoring\.internal|"
        r"автоматическ|noreply@jira|\[INFO\].*healthcheck",
        "авто-уведомление от системы",
    ),
    Rule(
        Category.INCIDENTS,
        r"URGENT|ERR_\d+|\b500\b|не работает|не отвечает|сбой|критич|"
        r"зависает при|не открывает|не запускается",
        "срочное обращение или инцидент",
    ),
    Rule(
        Category.ACCESS,
        r"доступ|vpn|уч[её]тн|парол|логин|права доступа|разрешени",
        "запрос доступа или учётной записи",
    ),
    Rule(
        Category.SOFTWARE,
        r"установ|обнов|chrome|adobe|excel|zoom|reader|программ|"
        r"приложени|лицензи",
        "установка или обновление ПО",
    ),
    Rule(
        Category.GENERAL,
        r"^Re:|^Fwd:|переслал|напоминан|отпуск|согласован|вопрос",
        "обычное обращение",
    ),
]
