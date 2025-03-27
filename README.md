# Azure Document Intelligence

This project extracts and analyzes PDF documents using Azure AI Document Intelligence. It provides a graphical user interface (GUI) for selecting input files, specifying output file names, and choosing the output directory.

## Setup

1. Clone the repository.
2. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your Azure API credentials:
   ```plaintext
   AZURE_API_KEY=your_azure_api_key
   AZURE_API_ENDPOINT=your_azure_api_endpoint
   ```

## Usage

1. Run the application:
   ```sh
   python src/main.py
   ```
2. Use the GUI to:
   - Select the input PDF file.
   - Enter the page number to extract.
   - Specify the output file name.
   - Choose the output directory where the Excel file will be saved.
3. Click the "Extract and Analyze" button to process the file.

## Features

- Extracts a specific page from a PDF file.
- Analyzes the extracted page using Azure AI Document Intelligence.
- Extracts tables from the document and saves them to an Excel file.
- Allows users to dynamically select the output directory and file name via the GUI.

## Requirements

- Python 3.7 or higher
- Azure AI Document Intelligence API credentials