import os


def load_images(instance, filename) -> str:
    """Помещает картинки скидок в отдельную папку"""
    path = "discount_images/"
    file_name = f'{instance.title}.{filename.split(".")[-1]}'
    return os.path.join(path, file_name)
