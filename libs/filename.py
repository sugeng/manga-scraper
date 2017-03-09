from slugify import Slugify

slugify_filename = Slugify()
slugify_filename.separator = ' '
slugify_filename.safe_chars = '~-._!'
slugify_filename.max_length = 255


def safe(name):
    return slugify_filename(name)
