import os
import unicodedata

# Directories
input_dir = "extracted_files"  # Directory containing the extracted .txt files
output_dir = "cleaned_files"  # Directory to save the cleaned .txt files
os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist

def normalize_to_utf(text):
    """
    Normalizes text to ensure it is UTF-8 compatible.
    Converts accented characters to ASCII equivalents where possible.
    """
    normalized_text = unicodedata.normalize('NFKD', text)
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

def clean_extracted_files(input_dir, output_dir):
    """
    Cleans all .txt files in the input directory and saves the cleaned content to the output directory.
    """
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_dir, filename)
            output_file_path = os.path.join(output_dir, filename)

            try:
                with open(input_file_path, 'r', encoding='utf-8', errors='replace') as infile, \
                     open(output_file_path, 'w', encoding='utf-8') as outfile:
                    
                    raw_text = infile.read()
                    cleaned_text = clean_text(raw_text)
                    outfile.write(cleaned_text)
                    print(f"Cleaned file saved: {output_file_path}")
            except Exception as e:
                print(f"Error cleaning file {filename}: {e}")

# Run the cleaning process
clean_extracted_files(input_dir, output_dir)

print(f"\nCleaning completed! Cleaned files saved in '{output_dir}'.")
