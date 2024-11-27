from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def wrap_text(text, text_width, canvas):
    """
    Splits the text into lines that fit within the given text width.
    """
    wrapped_lines = []
    words = text.split()
    current_line = ""

    for word in words:
        if canvas.stringWidth(current_line + " " + word, "Helvetica", 12) <= text_width:
            current_line += ("" if not current_line else " ") + word
        else:
            wrapped_lines.append(current_line)
            current_line = word
    if current_line:
        wrapped_lines.append(current_line)
    
    return wrapped_lines

def convert_txt_to_pdf(input_txt, output_pdf):
    """
    Converts a .txt file to a .pdf file using ReportLab, ensuring text wraps within page width.
    """
    try:
        # Create a PDF canvas
        c = canvas.Canvas(output_pdf, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica", 12)  # UTF-8 compatible font
        line_height = 14
        margin = 50  # Margin from both sides (left and right)
        text_width = width - 2 * margin  # Available width for text
        x, y = margin, height - margin  # Initial position for writing text

        # Read the text file line by line
        with open(input_txt, 'r', encoding='utf-8') as file:
            for line in file:
                # Wrap text to fit within the available width
                wrapped_lines = wrap_text(line.strip(), text_width, c)
                for wrapped_line in wrapped_lines:
                    if y < margin:  # If reaching the bottom margin, add a new page
                        c.showPage()
                        c.setFont("Helvetica", 12)
                        y = height - margin
                    c.drawString(x, y, wrapped_line)
                    y -= line_height

        # Save the PDF
        c.save()
        print(f"PDF created successfully: {output_pdf}")
    except Exception as e:
        print(f"Error converting {input_txt} to PDF: {e}")

# Example usage
input_txt = "extracted_content.txt"  # Path to the single .txt file
output_pdf = "extracted_content.pdf"  # Desired output PDF name
convert_txt_to_pdf(input_txt, output_pdf)
