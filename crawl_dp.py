import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque

# Define the base URL and visited links set
base_url = 'https://docs.ipfdev.co.uk/home/IPF_RELEASE_2024.3.0/home.html'
visited_links = set()
output_file = "crawled_links.txt"

def crawl_website_iteratively(base_url):
    # Queue for BFS traversal
    to_crawl = deque([base_url])

    with open(output_file, 'w') as file:
        while to_crawl:
            # Get the next URL to crawl
            current_url = to_crawl.popleft()

            # Skip if already visited
            if current_url in visited_links:
                continue

            print(f"Crawling: {current_url}")
            try:
                # Send a GET request
                response = requests.get(current_url, timeout=10)
                if response.status_code != 200:
                    print(f"Failed to retrieve: {current_url}, Status Code: {response.status_code}")
                    continue

                # Parse HTML content
                soup = BeautifulSoup(response.text, 'html.parser')

                # Save the URL to the output file
                file.write(current_url + '\n')

                # Mark as visited
                visited_links.add(current_url)

                # Extract and enqueue links
                for link in soup.find_all('a', href=True):
                    absolute_url = urljoin(current_url, link['href'])
                    if absolute_url.startswith('http') and absolute_url not in visited_links:
                        to_crawl.append(absolute_url)

            except requests.exceptions.RequestException as e:
                print(f"Error crawling {current_url}: {e}")

    print(f"\nCrawling completed! All visited links are saved in '{output_file}'.")

# Start crawling from the base URL
crawl_website_iteratively(base_url)
