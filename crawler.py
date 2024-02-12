import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def extract_links(url, base_url):
    """Extracts all valid links from a given URL, ensuring they stay within the same domain."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for error statuses

        soup = BeautifulSoup(response.content, 'html.parser')
        links = set()
        for link in soup.find_all('a'):
            new_url = urljoin(base_url, link.get('href'))

            # Filter for same domain and valid URLs
            if urlparse(new_url).netloc == urlparse(base_url).netloc:
                links.add(new_url)

        return links

    except requests.exceptions.RequestException as e:
        print(f"Error processing {url}: {e}")
        return set()

def crawl(start_url):
    """Crawls a website, discovering URLs recursively."""
    visited = set()
    pending = {start_url}

    while pending:
        url = pending.pop()
        if url not in visited:
            visited.add(url)

            print(f"Crawling: {url}")
            links = extract_links(url, start_url)
            pending.update(links - visited)  # Add new, unvisited links

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Website Crawler')
    parser.add_argument('-u', '--url', required=True, help='The starting URL to crawl')
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')

    args = parser.parse_args()

    crawl(args.url)
