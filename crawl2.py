import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Set to keep track of visited links
visited_links = set()
output_file = "crawled_links.txt"

def crawl_website(url):
    """
    Crawls the given URL, ignoring fragments, and saves all unique links to a file.
    """
    try:
        # Ignore URLs with fragments
        if "#" in url:
            url = url.split("#")[0]  # Strip the fragment to avoid duplicates

        # Check if the URL has already been visited
        if url in visited_links:
            return

        # Mark URL as visited
        visited_links.add(url)

        print(f"Crawling: {url}")
        # Send a GET request to the website
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Save the URL to the output file
            with open(output_file, 'a') as file:
                file.write(url + '\n')

            # Extract all hyperlinks on the page
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if href:
                    # Convert relative URLs to absolute
                    absolute_url = urljoin(url, href)
                    # Ignore fragments and revisit prevention
                    if "#" in absolute_url:
                        absolute_url = absolute_url.split("#")[0]
                    if absolute_url.startswith('http') and absolute_url not in visited_links:
                        crawl_website(absolute_url)  # Recursive call to follow links
        else:
            print(f"Failed to retrieve {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error crawling {url}: {e}")

# Example usage
base_url = "https://docs.ipfdev.co.uk/home/IPF_RELEASE_2024.3.0/home.html"
crawl_website(base_url)

print(f"\nCrawling completed! All unique links saved in '{output_file}'.")
