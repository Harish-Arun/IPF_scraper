import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

# Output file to save crawled image links
output_file_images = "crawled_image_links.txt"

# Set to keep track of visited links
visited_links = set()

def crawl_images_in_articles(start_url, release):
    """
    Iteratively crawls the given URL, processes only links within the target domain,
    and containing the release pattern, saving all unique image links within <article class="doc"> to a file.
    """
    # Use a queue for URLs to visit
    to_visit = deque([start_url])

    # Parse the target domain from the base URL
    target_domain = urlparse(start_url).netloc

    with open(output_file_images, 'w') as file:  # Open file once for writing
        while to_visit:
            # Get the next URL from the queue
            url = to_visit.popleft()

            # Ignore URLs with fragments
            if "#" in url:
                url = url.split("#")[0]

            # Skip if already visited
            if url in visited_links:
                continue

            # Mark as visited
            visited_links.add(url)

            print(f"Crawling: {url}")
            try:
                # Send a GET request
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Extract and save image links within <article class="doc">
                    articles = soup.find_all('article', class_="doc")
                    for article in articles:
                        images = article.find_all('img')
                        for img in images:
                            img_src = img.get('src')
                            if img_src:
                                absolute_img_url = urljoin(url, img_src)
                                file.write(absolute_img_url + '\n')

                    # Extract all hyperlinks and add them to the queue
                    links = soup.find_all('a')
                    for link in links:
                        href = link.get('href')
                        if href:
                            absolute_url = urljoin(url, href)
                            # Ignore fragments
                            if "#" in absolute_url:
                                absolute_url = absolute_url.split("#")[0]
                            # Check if the link belongs to the target domain and contains the release pattern
                            if (
                                absolute_url.startswith('http') and
                                urlparse(absolute_url).netloc == target_domain and
                                release in absolute_url and
                                absolute_url not in visited_links
                            ):
                                to_visit.append(absolute_url)
                else:
                    print(f"Failed to retrieve {url}. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error crawling {url}: {e}")

# Example usage
base_url = "https://docs.ipfdev.co.uk/home/IPF_RELEASE_2024.3.0/home.html"
release_pattern = "IPF_RELEASE_2024.3.0"  # Specify the release pattern to filter URLs
crawl_images_in_articles(base_url, release_pattern)

print(f"\nCrawling completed! All unique image links from '<article class=\"doc\">' saved in '{output_file_images}'.")
