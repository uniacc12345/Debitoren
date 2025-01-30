from pypdf import PdfReader, PdfWriter
import re
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()  # Hide the main window

input_pdf_path = filedialog.askopenfilename(title="Wähle die zu teilende PDF Datei.")
output_dir = filedialog.askdirectory(title="Wähle den Ordner in der die geteilten PDFs gespeichert werden sollen")


#input_pdf_path = "Documents/test_doc.pdf"
#output_dir = "Documents/SplitTest/"  # Update with your output folder


reader = PdfReader(input_pdf_path)
reports = {}
current_report = None

for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        lines = text.split("\n")

        if len(lines) > 3:
            if lines[2].strip().startswith("ApoIK: "):
                current_report = (lines[2].strip(), lines[3].strip())
                reports[current_report] = []

        if current_report:
            reports[current_report].append(page)

for (line2, line3), pages in reports.items():
    writer = PdfWriter()
    for page in pages:
        writer.add_page(page)

    safe_line3 = re.sub(
        r"\b(Apotheke|Apotheken|Rotpunkt|TopPharm|AG|GmbH|AA1|am|Andres|Vitalis|" +
        r"in|TP|und|Drogerie|zum|zur|Pfungen|Baar|Lindenapotheke|Küsnacht|Dietikon|Kloten|Neuhausen|Volksapotheke|" +
        r"Parfümerie)\b",
        "",
        line3
    )

    safe_line3 = safe_line3.replace("&", "")
    safe_line3 = safe_line3.replace("Dr.", "")
    safe_line3 = safe_line3.replace("Zuger Kantonsspital", "ZGKS")
    safe_line3 = re.sub(r"-", " ", safe_line3)  # Replace hyphens with space
    safe_line3 = re.sub(r"\s+", " ", safe_line3).strip()



    output_path = f"{output_dir}/{safe_line3}.pdf"

    with open(output_path, "wb") as output_file:
        writer.write(output_file)
