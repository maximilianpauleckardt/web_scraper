from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict
import aiohttp
import asyncio

class AsyncCrawler:
    def __init__(self, base_url, max_concurrency, max_pages):
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc
        self.page_data = {}
        self.visited = set()
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        
        async with self.lock: 
            if self.should_stop is True:
                return False
            if len(self.visited) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                
                return False
            if normalized_url in self.visited:
                return False
            self.visited.add(normalized_url)
            return True

    async def get_html(self, url):
        async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as response:
            if 400 <= response.status:
                raise Exception(f"Status code is {response.status}")
            content_type = response.headers.get("Content-Type", "")
            if not content_type.startswith("text/html"):
                raise Exception("Content-Type is not text/html")
            return await response.text()
        
    async def crawl_page(self, current_url):
        if self.should_stop is True:
            return self.page_data
    
        # 1. Stay on domain
        if urlsplit(current_url).netloc != self.base_domain:
            return

        # 2. Prevent crawling the same page twice
        normalized_url = normalize_url(current_url)
        is_new = await self.add_page_visit(normalized_url)
        if not is_new:
            return
        
        async with self.semaphore:
            
            # 3. Fetch and extract page data
            print(f"Crawling: {current_url}")
            try:
                html = await self.get_html(current_url)
            except Exception as e:
                print(f"Error fetching {current_url}: {e}")
                return self.page_data

            extracted_data = extract_page_data(html, current_url)
            
            async with self.lock:
                self.page_data[normalized_url] = extracted_data
        
        if self.should_stop is True:
            return self.page_data
        
        # 4. Recursively crawl outgoing links
        tasks = []
        for link in extracted_data["outgoing_links"]:
            task = asyncio.create_task(self.crawl_page(link))
            tasks.append(task)
            self.all_tasks.add(task)
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        finally:
            for task in tasks: 
                self.all_tasks.discard(task)
                
        return self.page_data
        
    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data

async def crawl_site_async(starting_url,max_concurrency, max_pages):
    async with AsyncCrawler(starting_url, max_concurrency, max_pages) as crawler:
        return await crawler.crawl()

def normalize_url(url: str) -> str:
    split_url = urlsplit(url)
    normalized_url = str(split_url.netloc + split_url.path)
    normalized_url = normalized_url.rstrip("/")
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