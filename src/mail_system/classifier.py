from .models import Category, ClassificationResult, Email
from .rules import RULES


class RuleBasedClassifier:
    def classify(self, email: Email) -> ClassificationResult:
        text = f"{email.subject}\n{email.body}\n{email.sender}"

        for rule in RULES:
            if rule.pattern.search(text):
                return ClassificationResult(
                    category=rule.category,
                    reason=rule.reason,
                )

        return ClassificationResult(
            category=Category.UNCLASSIFIED,
            reason="ни одно правило не подошло",
        )
