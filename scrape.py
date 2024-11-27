import requests
from bs4 import BeautifulSoup

# Define the URL to scrape
url = 'https://docs.ipfdev.co.uk/home/IPF_RELEASE_2024.3.0/home.html'

try:
    # Send a GET request to the website
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the page title
        page_title = soup.title.string if soup.title else "No Title Found"
        print(f"Page Title: {page_title}\n")

        # Extract all hyperlinks (anchor tags)
        print("Links on the Page:")
        links = soup.find_all('a')
        for idx, link in enumerate(links, start=1):
            href = link.get('href')
            text = link.get_text(strip=True)
            print(f"{idx}. Text: {text or 'No Text'}, URL: {href or 'No URL'}")

        # Example: Extract all paragraph text
        print("\nParagraph Texts:")
        paragraphs = soup.find_all('p')
        for idx, paragraph in enumerate(paragraphs, start=1):
            print(f"{idx}. {paragraph.get_text(strip=True)}")
    else:
        print(f"Failed to retrieve the page. Status Code: {response.status_code}")
except Exception as e:
    print(f"An error occurred: {e}")
