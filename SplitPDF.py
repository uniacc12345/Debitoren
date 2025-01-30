from pypdf import PdfReader, PdfWriter

def split(path, name_of_split):
    pdf = PdfReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfWriter()
        pdf_writer.addPage(pdf.getPage(page))

        output = f'{name_of_split}{page}.pdf'
        with open(output, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)