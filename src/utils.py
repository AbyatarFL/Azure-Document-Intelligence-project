from PyPDF2 import PdfReader, PdfWriter
import pandas as pd
from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
from bs4 import BeautifulSoup
import os
from io import StringIO

def extract_pages(pdf_path, page_number):
    """
    Extracts a specific page from a PDF file and saves it as a new PDF file.
    """
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    max_pages = len(reader.pages)

    if not (1 <= page_number <= max_pages):
        print(f"❌ Error: PDF hanya memiliki {max_pages} halaman!")
        return None

    writer.add_page(reader.pages[page_number - 1])

    output_pdf = f"halaman_ekstrak_{page_number}.pdf"
    with open(output_pdf, "wb") as f:
        writer.write(f)

    return output_pdf

def analyze_pdf_or_image(fileOK, output_filepath):
    """
    Analyzes the extracted PDF page and saves the extracted data to an Excel file.
    """
    try:
        print("📄 Menganalisis PDF...")

        # Load the document using Azure AI Document Intelligence
        loader = AzureAIDocumentIntelligenceLoader(
            file_path=fileOK,
            api_key=os.getenv("AZURE_API_KEY"),
            api_endpoint=os.getenv("AZURE_API_ENDPOINT"),
            api_model="prebuilt-layout"
        )

        docs = loader.load()
        print("✅ Loader berhasil!")

        # Combine all text from the document
        extracted_text = " ".join([page.page_content for page in docs])

        # Use BeautifulSoup to extract HTML tables
        soup = BeautifulSoup(extracted_text, "html.parser")
        tables = soup.find_all("table")

        if not tables:
            print("⚠️ Tidak ada tabel yang ditemukan dalam dokumen.")
            return

        # Save the extracted tables to an Excel file
        with pd.ExcelWriter(output_filepath, engine="xlsxwriter") as writer:
            for i, table in enumerate(tables):
                # Wrap the table in StringIO to avoid FutureWarning
                df = pd.read_html(StringIO(str(table)))[0]

                # Flatten MultiIndex columns if present
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = ['_'.join(map(str, col)).strip() for col in df.columns]

                df.reset_index(drop=True, inplace=True)  # Avoid MultiIndex errors
                df.to_excel(writer, sheet_name=f"Table_{i+1}", index=False)
                print(f"✅ Tabel disimpan di sheet 'Table_{i+1}'.")

        print(f"✅ Hasil berhasil disimpan di {output_filepath}")

    except FileNotFoundError:
        print(f"❌ File '{fileOK}' tidak ditemukan")

    except Exception as e:
        print(f"❌ Terjadi kesalahan: {str(e)}")