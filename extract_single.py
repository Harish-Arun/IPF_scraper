import requests
from bs4 import BeautifulSoup

# Input file containing crawled links
input_file = "crawled_links.txt"

# Output file to save extracted content with URLs
output_file = "extracted_content.txt"

def extract_content_with_url(input_file, output_file):
    """
    Extracts content from the <article class="doc"> tag of each URL in the input file
    and appends it, along with the URL, to the output file.
    """
    with open(input_file, 'r') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
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

                        # Write the URL and its content to the output file
                        outfile.write(f"=== URL: {url} ===\n")
                        outfile.write(article_content)
                        outfile.write("\n" + "=" * 50 + "\n\n")  # Extra newline here
                    else:
                        print(f"No <article class='doc'> found in {url}")
                else:
                    print(f"Failed to fetch {url}. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error extracting content from {url}: {e}")

# Run the extraction
extract_content_with_url(input_file, output_file)

print(f"\nExtraction completed! All content saved in '{output_file}'.")
