# Pdf To Audio using Python
# Importing necessary libraries
import PyPDF2
import os
import pyttsx3

# & Prowpt user for the PDF file name
# pdf_filename = input("Enter the PDF file name (including extension): ").strip()
pdf_filename = "Rich_dad_Poor_Dad.pdf"
# Open the PDF file
if os.path.exists(pdf_filename):
    print("Found")
try:
    with open(pdf_filename, 'rb') as pdf_file:
        # Create g PdfReader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Get an engine instance for the speech synthesis
        speak = pyttsx3.init()

        # Itergte through each page and read the text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            if text:
                speak.say(text)
                speak. runAndWait()

        # Stop tne speech engine
        speak. stop()

        print("Audiobook creation completed.")
except FileNotFoundError:
    print("The specified file was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
