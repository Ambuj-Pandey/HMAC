import fitz


# this is to extract text be it handwritten or digital
def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text.replace(' ', '').replace('\n', ',')

#save it in .txt form but each word is on new line
def save_text_to_file(text, output_path):
    with open(output_path, 'w') as file:
        file.write(text)

#input pdf path
pdf_path = '/content/drive/MyDrive/BERT/pdfFiles/cmp1.pdf'

#extracts text from pdf and converts to comma seperated text(not saved in a file yet, its a string) 
pdf_text = extract_text_from_pdf(pdf_path)

#save string from 'pdf_text' to the file at the location given at the second parameter
save_text_to_file(pdf_text, '/content/drive/MyDrive/BERT/textDetectionOutput/Output1.txt')