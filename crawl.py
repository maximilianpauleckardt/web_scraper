from urllib.parse import urlsplit
from bs4 import BeautifulSoup, Tag

def normalize_url(url: str) -> str:
    split_url = urlsplit(url)
    normalized_url = str(split_url.netloc + split_url.path)
    if normalized_url[-1] == "/": normalized_url = normalized_url.rstrip("/")
    return normalized_url.lower()

def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html,'html.parser')
    h_tag = soup.find('h1')
    if h_tag: 
        return h_tag.get_text(strip=True) 
    h_tag = soup.find('h2')
    return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""
    

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html,'html.parser')
    main_tag = soup.find('main')
    if main_tag:
        p_tag = main_tag.find('p')
        if p_tag: 
            return p_tag.get_text(strip=True) 
    p_tag = soup.find('p')
    return p_tag.get_text(strip=True) if isinstance(p_tag, Tag) else ""
