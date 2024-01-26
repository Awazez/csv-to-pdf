import os
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_location_pdf(df, location):
    # Filter the data for the current location
    filtered_df = df[df['localisation'] == location]

    # Create PDF
    pdf_filename = os.path.join(output_folder, f'{location}.pdf')
    pdf = canvas.Canvas(pdf_filename, pagesize=letter)

    # Set font and size
    pdf.setFont("Helvetica", 12)

    # Constants
    LINE_HEIGHT = 20
    PAGE_WIDTH, PAGE_HEIGHT = letter
    MAX_CHARACTERS_PER_COLUMN = 10

    # Write header
    pdf.drawString(100, PAGE_HEIGHT - 50, f"Filtered Data for {location}")

    # Write filtered data to PDF
    y_position = PAGE_HEIGHT - 70
    current_row = 0

    for index, row in filtered_df.iterrows():
        if current_row % (int((PAGE_HEIGHT - 70) / LINE_HEIGHT)) == 0 and current_row != 0:
            pdf.showPage()  # Start a new page
            y_position = PAGE_HEIGHT - 50

            # Write header on the new page
            pdf.setFont("Helvetica", 12)
            pdf.drawString(100, y_position, f"Filtered Data for {location}")
            y_position -= 20  # Adjust y-position for data on the new page

        y_position -= LINE_HEIGHT
        # Truncate each column to a maximum of 10 characters
        truncated_text = ", ".join(str(row[col])[:MAX_CHARACTERS_PER_COLUMN] for col in ['titre', 'auteur', 'code barre', 'cote', 'nombre de prets'])
        pdf.drawString(100, y_position, truncated_text)
        current_row += 1

    # Save the PDF
    pdf.save()
    print(f"PDF saved as {pdf_filename}")

if __name__ == "__main__":
    # Read CSV file
    try:
        df = pd.read_csv('source.csv')
    except FileNotFoundError:
        print("CSV file not found. Make sure the file path is correct.")
        exit(1)
    except pd.errors.EmptyDataError:
        print("CSV file is empty. Please check the file.")
        exit(1)
    except pd.errors.ParserError:
        print("Error parsing CSV file. Ensure the file has the correct format.")
        exit(1)

    # Get unique locations from the 'localisation' column
    unique_locations = df['localisation'].unique()

    # Create the 'output' folder if it doesn't exist
    output_folder = 'output'
    os.makedirs(output_folder, exist_ok=True)

    for location in unique_locations:
        generate_location_pdf(df, location)