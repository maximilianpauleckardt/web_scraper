from urllib.parse import urlsplit

def normalize_url(url: str) -> str:
    split_url = urlsplit(url)
    normalized_url = str(split_url.netloc + split_url.path)
    if normalized_url[-1] == "/": normalized_url = normalized_url.rstrip("/")
    return normalized_url.lower()

