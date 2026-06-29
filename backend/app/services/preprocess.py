import html
import re


URL_PATTERN = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
WORD_PATTERN = re.compile(r"[A-Za-z][A-Za-z'-]*")


def normalize_text(text: str) -> str:
    """Normalize article text while keeping enough signal for the classifier."""
    unescaped = html.unescape(text or "")
    without_urls = URL_PATTERN.sub(" URL ", unescaped)
    compact = re.sub(r"\s+", " ", without_urls)
    return compact.strip().lower()


def text_stats(text: str) -> dict[str, float | int]:
    words = WORD_PATTERN.findall(text or "")
    uppercase_words = [word for word in words if len(word) > 1 and word.isupper()]
    return {
        "characters": len(text or ""),
        "words": len(words),
        "urls": len(URL_PATTERN.findall(text or "")),
        "exclamations": (text or "").count("!"),
        "questions": (text or "").count("?"),
        "uppercase_ratio": len(uppercase_words) / max(len(words), 1),
    }
