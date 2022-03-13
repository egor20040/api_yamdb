
from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_score(value):
    if value > 10 or value < 1:
        raise ValidationError(
            ('Рейтинг %(value)s не коректный!'),
        )


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            ('Год %(value)s не коректный!'),
            params={'value': value},
        )
