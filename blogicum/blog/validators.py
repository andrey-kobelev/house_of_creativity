from django.core.exceptions import ValidationError
from string import ascii_letters


def is_username_english(value: str) -> None:
    for letter in value:
        if letter not in ascii_letters:
            raise ValidationError(
                'Вводите имя пользователя тольо латинскими буквами!'
            )
