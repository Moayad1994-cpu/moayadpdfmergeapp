from pywebio.input import file_upload, input
from pywebio.output import put_html, put_markdown, put_text, put_buttons, put_file, toast
from pywebio import start_server
from PyPDF2 import PdfMerger, PdfReader
import os

def merge_pdf_files():
    """
    Web-based PDF merger with file preview and enhanced UI.
    """
    # Add custom CSS for better styling
    put_html("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(to bottom right, #ffffff, #f0f8ff);
            color: #333;
            margin: 0;
            padding: 0;
        }
        .container {
            text-align: center;
            padding: 20px;
            margin-top: 20px;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            max-width: 700px;
            margin: auto;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }
        h1 {
            color: #007bff;
            font-size: 2.5em;
        }
        button {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
        }
        button:hover {
            background-color: #0056b3;
        }
        .preview-container {
            background: #f9f9f9;
            padding: 15px;
            margin: 20px auto;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            text-align: left;
        }
        .file-content {
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            color: #555;
            overflow-y: auto;
            max-height: 200px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #ffffff;
        }
    </style>
    <div class="container">
        <h1>Developed By <p1>Moayad Dughmosh</p1></h1>
        <h1>Merge PDF Files</h1>
        <p>Upload multiple PDF files to preview and merge them into one.</p>
    </div>
    """)

    # File upload input
    files = file_upload("Select PDF files to merge", accept="application/pdf", multiple=True)
    if not files:
        put_text("No files selected. Please upload PDF files to continue.")
        return

    # Preview PDF files before merging
    put_markdown("### PDF Previews:")
    temp_files = []
    for file in files:
        temp_file_path = file['filename']
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(file['content'])
        temp_files.append(temp_file_path)

        # Read PDF content for preview
        put_markdown(f"**File:** {temp_file_path}")
        try:
            reader = PdfReader(temp_file_path)
            content = ""
            for page in reader.pages[:2]:  # Limit to first 2 pages
                content += page.extract_text()
            put_html(f"<div class='file-content'>{content or 'Unable to extract text from this file.'}</div>")
        except Exception as e:
            put_text(f"Could not preview file: {temp_file_path}. Error: {e}")

    # Ask for new filename
    new_filename = input("Enter a new name for the merged PDF file:", type="text", placeholder="e.g., MergedFile.pdf")
    new_filename = new_filename if new_filename.endswith(".pdf") else f"{new_filename}.pdf"

    try:
        # Create a PdfMerger object
        merger = PdfMerger()

        # Add files to the merger
        for temp_file_path in temp_files:
            merger.append(temp_file_path)

        # Save the merged PDF to a temporary file
        merged_file_path = new_filename
        merger.write(merged_file_path)
        merger.close()

        # Provide the merged PDF as a downloadable file
        with open(merged_file_path, "rb") as merged_file:
            put_file(new_filename, merged_file.read())

        # Cleanup temporary files
        for temp_file_path in temp_files:
            os.remove(temp_file_path)
        os.remove(merged_file_path)

        toast(f"Files merged successfully! Download your file: {new_filename}")

    except Exception as e:
        put_text(f"An error occurred: {e}")

# Start the PyWebIO server
if __name__ == "__main__":
    start_server(merge_pdf_files, port=34345, debug=True)
