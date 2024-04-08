import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Set of all unique links found
all_links = set()

def extract_links(url):
    """
    Extracts and returns all unique links from a given URL.
    """
    global all_links
    
    # Make an HTTP request to get the HTML content
    response = requests.get(url)
    if response.status_code != 200:
        return
    
    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract links from 'href' attributes of <a> tags
    for link in soup.find_all('a', href=True):
        href = link['href'].strip()
        if href.startswith('http'):  # External link
            print("External link:", href)
        else:
            # Convert relative URLs to absolute URLs
            href = urljoin(url, href)
            all_links.add(href)
    
    # Extract links from 'src' attributes of various tags
    for tag in soup.find_all(['img', 'script', 'link'], src=True):
        src = tag['src'].strip()
        if src.startswith('http'):  # External link
            print("External link:", src)
        else:
            # Convert relative URLs to absolute URLs
            src = urljoin(url, src)
            all_links.add(src)

def crawl_internal_links(url):
    """
    Crawls internal links recursively and extracts all unique links.
    """
    global all_links
    
    # Extract links from the current URL
    extract_links(url)
    
    # Parse the base URL
    parsed_url = urlparse(url)
    base_url = parsed_url.scheme + '://' + parsed_url.netloc
    
    # Find all unique internal links
    internal_links = {link for link in all_links if urlparse(link).netloc == parsed_url.netloc}
    
    # Recursively crawl internal links
    for link in internal_links:
        if link not in all_links:
            crawl_internal_links(link)

# Start crawling from the provided initial URL
initial_url = 'https://krittikaiitb.github.io'
crawl_internal_links(initial_url)

# Print all unique links found
print("All unique links found:")
for link in all_links:
    print(link)
