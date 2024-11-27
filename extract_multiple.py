import requests
from bs4 import BeautifulSoup
import os
import re

# Input file containing crawled links
input_file = "crawled_links.txt"

# Output directory to store extracted content
output_dir = "extracted_files"
os.makedirs(output_dir, exist_ok=True)

def sanitize_filename(url):
    """
    Sanitizes a URL to create a valid filename.
    """
    return re.sub(r'[^\w\-_\.]', '_', url)  # Replace invalid characters with '_'

def extract_content_to_separate_files(input_file, output_dir):
    """
    Extracts content from the <article class="doc"> tag of each URL in the input file
    and saves it into separate files named after the URL.
    """
    with open(input_file, 'r') as infile:
        urls = infile.readlines()

        for idx, url in enumerate(urls, start=1):
            url = url.strip()
            print(f"Extracting content from URL {idx}/{len(urls)}: {url}")
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Extract the <article class="doc"> tag
                    article = soup.find('article', class_='doc')
                    if article:
                        # Extract textual content from the article
                        article_content = article.get_text(separator="\n", strip=True)

                        # Generate a sanitized filename based on the URL
                        sanitized_filename = sanitize_filename(url) + ".txt"
                        output_file = os.path.join(output_dir, sanitized_filename)

                        # Save the content to a file
                        with open(output_file, 'w', encoding='utf-8') as outfile:
                            outfile.write(f"=== URL: {url} ===\n")
                            outfile.write(article_content)
                            outfile.write("\n")
                        print(f"Saved content to {output_file}")
                    else:
                        print(f"No <article class='doc'> found in {url}")
                else:
                    print(f"Failed to fetch {url}. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error extracting content from {url}: {e}")

# Run the extraction
extract_content_to_separate_files(input_file, output_dir)

print(f"\nExtraction completed! All content saved in '{output_dir}'.")
