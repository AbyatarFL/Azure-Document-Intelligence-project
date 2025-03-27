import os
from utils import extract_pages, analyze_pdf_or_image
from dotenv import load_dotenv
import tkinter as tk
from tkinter import filedialog, messagebox

# Load environment variables from .env file
load_dotenv()

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        pdf_filename.set(file_path)
        print(f"✅ File '{file_path}' ditemukan.")

def select_output_directory():
    directory = filedialog.askdirectory()
    if directory:
        output_directory.set(directory)
        print(f"✅ Output directory set to '{directory}'.")

def extract_and_analyze():
    file_path = pdf_filename.get()
    if not os.path.exists(file_path):
        messagebox.showerror("Error", f"❌ File '{file_path}' tidak ditemukan.")
        return

    output_dir = output_directory.get()
    if not os.path.exists(output_dir):
        messagebox.showerror("Error", f"❌ Output directory '{output_dir}' tidak ditemukan.")
        return

    output_filename = output_filename_entry.get()
    if not output_filename.endswith(".xlsx"):
        output_filename += ".xlsx"

    output_filepath = os.path.join(output_dir, output_filename)

    try:
        # Extract a single page
        page_number = int(page_number_entry.get())
        extracted_pdf = extract_pages(file_path, page_number)
        if extracted_pdf:
            analyze_pdf_or_image(extracted_pdf, output_filepath)
            os.remove(extracted_pdf)  # Delete the temporary PDF file
        messagebox.showinfo("Success", f"✅ Hasil berhasil disimpan di {output_filepath}")
    except ValueError:
        messagebox.showerror("Error", "❌ Nomor halaman harus berupa angka.")
    except Exception as e:
        messagebox.showerror("Error", f"❌ Terjadi kesalahan: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("Azure Document Intelligence")

# Create and place widgets
tk.Label(root, text="Pilih file PDF:").grid(row=0, column=0, padx=10, pady=10)
pdf_filename = tk.StringVar()
tk.Entry(root, textvariable=pdf_filename, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=10)

# Input for page number
tk.Label(root, text="Masukkan nomor halaman:").grid(row=1, column=0, padx=10, pady=10)
page_number_entry = tk.Entry(root, width=50)
page_number_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Nama file output:").grid(row=2, column=0, padx=10, pady=10)
output_filename_entry = tk.Entry(root, width=50)
output_filename_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Pilih folder output:").grid(row=3, column=0, padx=10, pady=10)
output_directory = tk.StringVar()
tk.Entry(root, textvariable=output_directory, width=50).grid(row=3, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_output_directory).grid(row=3, column=2, padx=10, pady=10)

tk.Button(root, text="Extract and Analyze", command=extract_and_analyze).grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Run the application
root.mainloop()