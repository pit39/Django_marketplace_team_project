from typing import Type
from transliterate import detect_language, translit

from . import models


def get_path(instance: Type['models.Category'], filename: str) -> str:
    """Возращает путь к файлу."""
    file_type: str = filename.split('.')[-1]
    return '{}/{}.{}'.format(
        'category',
        instance.name,
        file_type,
    )


def get_slug(name: str) -> str:
    """Возвращает строку slug."""

    slug: str = name if ' ' not in name else '-'.join(name.split())
    if detect_language(slug) == 'ru':
        slug = translit(slug, reversed=True)
    return slug
