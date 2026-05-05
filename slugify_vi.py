"""Custom Vietnamese-aware slugify using stdlib only."""

import re
import unicodedata


def _slugify(text, sep="-"):
    # Đ/đ does not decompose via NFKD, handle explicitly
    text = str(text).replace("Đ", "D").replace("đ", "d")
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode()
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", sep, text).strip(sep)
    return text


class _Slugifier:
    def __init__(self, sep="-"):
        self.sep = sep

    def __call__(self, text, sep=None):
        return _slugify(text, sep if sep is not None else self.sep)


def slugify(**kwargs):
    """Return a slugify function compatible with the toc extension."""
    return _Slugifier(sep=kwargs.get("sep", "-"))
