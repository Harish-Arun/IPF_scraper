from fpdf import FPDF
import os

def convert_txt_to_pdf(input_txt, output_pdf):
    """
    Converts a single .txt file to a .pdf file, supporting UTF-8 characters.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.add_font('FreeSerif', '', os.path.join(os.path.dirname(__file__), 'FreeSerif.ttf'), uni=True)
    pdf.set_font("FreeSerif", size=12)  # Use a font that supports UTF-8

    try:
        with open(input_txt, 'r', encoding='utf-8') as file:
            for line in file:
                pdf.multi_cell(0, 10, line.strip())  # Add line to PDF
        pdf.output(output_pdf)
        print(f"PDF created successfully: {output_pdf}")
    except Exception as e:
        print(f"Error converting {input_txt} to PDF: {e}")

# Example usage
input_txt = "extracted_content.txt"  # Path to the single .txt file
output_pdf = "extracted_content_copy.pdf"  # Desired output PDF name
convert_txt_to_pdf(input_txt, output_pdf)
