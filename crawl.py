import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Define the base URL and visited links set
base_url = 'https://docs.ipfdev.co.uk/home/IPF_RELEASE_2024.3.0/home.html'
visited_links = set()

# Output file to save the links
output_file = "crawled_links.txt"

def crawl_website(url):
    # If the URL has already been visited, skip it
    if url in visited_links:
        return
    
    # Add the URL to the visited set
    visited_links.add(url)
    print(f"Crawling: {url}")
    
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Save the URL to the output file
            with open(output_file, 'a') as file:
                file.write(url + '\n')
            
            # Extract all hyperlinks on the page
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if href:
                    # Resolve relative URLs to absolute URLs
                    absolute_url = urljoin(url, href)
                    
                    # Filter out non-HTTP(S) links and revisit prevention
                    if absolute_url.startswith('http'):
                        crawl_website(absolute_url)  # Recursively crawl
        else:
            print(f"Failed to retrieve: {url}, Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while crawling {url}: {e}")

# Start crawling from the base URL
crawl_website(base_url)

# Print completion message
print(f"\nCrawling completed! All visited links are saved in '{output_file}'.")
