from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict
import requests

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

def get_urls_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    for tag in soup.find_all('a'):
        path = tag.get('href')
        if path is not None:
            results.append(urljoin(base_url, path))
    return results

def get_images_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    for tag in soup.find_all('img'):
        path = tag.get('src')
        if path is not None:
            results.append(urljoin(base_url, path))
    return results

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

def extract_page_data(html: str, page_url: str) -> PageData:
    page_data = {}
    page_data["url"] = page_url
    page_data["heading"] = get_heading_from_html(html)
    page_data["first_paragraph"] = get_first_paragraph_from_html(html)
    page_data["outgoing_links"] = get_urls_from_html(html, page_url)
    page_data["image_urls"] = get_images_from_html(html, page_url)
    return page_data

def get_html(url):
    response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    if 400 <= response.status_code:
        raise Exception(f"Status code is {response.status_code}")
    if not response.headers["Content-Type"].startswith("text/html"):
        raise Exception("Content-Type is not text/html")
    return response.text

def crawl_page(base_url, current_url=None, page_data=None):
    if current_url is None:
        current_url = base_url
    if page_data is None:
        page_data = {}

    # 1. Stay on domain
    if urlsplit(base_url).netloc != urlsplit(current_url).netloc:
        return page_data

    # 2. Prevent crawling the same page twice
    normalized_url = normalize_url(current_url)
    if normalized_url in page_data:
        return page_data

    # 3. Fetch and extract page data
    print(f"Crawling: {current_url}")
    try:
        html = get_html(current_url)
    except Exception as e:
        print(f"Error fetching {current_url}: {e}")
        return page_data

    extracted_data = extract_page_data(html, current_url)
    page_data[normalized_url] = extracted_data

    # 4. Recursively crawl outgoing links
    for link in extracted_data["outgoing_links"]:
        page_data = crawl_page(base_url, link, page_data)

    return page_data
                    
                   