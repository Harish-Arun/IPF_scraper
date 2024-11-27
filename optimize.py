import unicodedata

def normalize_to_utf(text):
    """
    Normalizes text to ensure it is UTF-8 compatible.
    Converts accented characters to ASCII equivalents where possible.
    """
    # Normalize to 'NFKD' to decompose characters like accents
    normalized_text = unicodedata.normalize('NFKD', text)
    # Encode to ASCII and ignore non-UTF characters
    utf_text = normalized_text.encode('ascii', 'ignore').decode('utf-8')
    return utf_text

def replace_unknown_characters(text):
    """
    Replaces unknown characters with a placeholder (e.g., '?').
    """
    return text.encode('utf-8', 'replace').decode('utf-8')

def clean_text(raw_text):
    """
    Cleans and optimizes the raw text using UTF-8 normalization and unknown character replacement.
    """
    raw_text = normalize_to_utf(raw_text)  # Step 1: Normalize to UTF-8
    raw_text = replace_unknown_characters(raw_text)  # Step 2: Replace unknown characters
    return raw_text

def clean_extracted_file(input_file, output_file):
    """
    Cleans the input file by ensuring UTF-8 compatibility and removing unknown characters.
    Saves the cleaned content to a new file.
    """
    try:
        with open(input_file, 'r', encoding='utf-8', errors='replace') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            
            raw_text = infile.read()
            cleaned_text = clean_text(raw_text)
            outfile.write(cleaned_text)
            print(f"Cleaned text saved to: {output_file}")
    except Exception as e:
        print(f"Error cleaning file: {e}")

# Example usage
input_file = "extracted_content.txt"  # Path to the raw text file
output_file = "cleaned_extracted_content.txt"  # Path to save the cleaned file
clean_extracted_file(input_file, output_file)
