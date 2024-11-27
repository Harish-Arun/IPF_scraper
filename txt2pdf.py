from fpdf import FPDF

def convert_txt_to_pdf(input_txt, output_pdf):
    """
    Converts a single .txt file to a .pdf file.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

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
output_pdf = "extracted_content.pdf"  # Desired output PDF name
convert_txt_to_pdf(input_txt, output_pdf)
