import os
import zipfile
import shutil
import xml.etree.ElementTree as ET
import fitz  # PyMuPDF for handling PDF documents
import docx  # python-docx for handling Word documents
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

# Function to read specifications from a text file
def read_specifications(spec_file):
    with open(spec_file, 'r') as file:
        specs = file.readlines()
    specs = [spec.strip() for spec in specs if spec.strip()]  # Remove empty lines
    return specs

# Function to scan PDF files for the specifications
def scan_pdf(file_path, specs):
    found_specs = []
    try:
        doc = fitz.open(file_path)  # Open the PDF with PyMuPDF
        text = ""
        for page in doc:
            text += page.get_text()  # Extract text from each page of the PDF
        for spec in specs:
            if re.search(re.escape(spec), text, re.IGNORECASE):
                found_specs.append(spec)  # Check if the specification is found in the text
    except Exception as e:
        print(f"Error scanning PDF {file_path}: {e}")
    return found_specs

# Function to scan Word documents for the specifications
def scan_word(file_path, specs):
    found_specs = []
    try:
        doc = docx.Document(file_path)  # Open the Word document
        text = "\n".join([para.text for para in doc.paragraphs])  # Extract text from all paragraphs
        for spec in specs:
            if re.search(re.escape(spec), text, re.IGNORECASE):
                found_specs.append(spec)
    except Exception as e:
        print(f"Error scanning Word document {file_path}: {e}")
    return found_specs

# Function to scan Markdown files for the specifications
def scan_markdown(file_path, specs):
    found_specs = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()  # Read the entire Markdown file
        for spec in specs:
            if re.search(re.escape(spec), text, re.IGNORECASE):
                found_specs.append(spec)
    except Exception as e:
        print(f"Error scanning Markdown {file_path}: {e}")
    return found_specs

def extract_text_from_pages(file_path):
    temp_dir = 'extracted_pages_content'
    text_content = []
    
    try:
        # Unzip the .pages file to extract its contents
        with zipfile.ZipFile(file_path, 'r') as z:
            z.extractall(temp_dir)
        
        # Search for XML files within the extracted directory
        for root_dir, dirs, files in os.walk(temp_dir):
            for file_name in files:
                if file_name.endswith(".xml"):
                    xml_file_path = os.path.join(root_dir, file_name)
                    try:
                        # Parse the XML file
                        tree = ET.parse(xml_file_path)
                        root = tree.getroot()
                        # Append the text content from the XML tree to the list
                        text_content.append(''.join(root.itertext()))
                    except ET.ParseError as e:
                        print(f"Error parsing XML file {xml_file_path}: {e}")
                    except Exception as e:
                        print(f"Unexpected error processing XML file {xml_file_path}: {e}")

        # Check if we found any text content
        if text_content:
            text = "\n".join(text_content)  # Combine all text into a single string
        else:
            raise FileNotFoundError("No XML content found in the .pages file")

    except zipfile.BadZipFile:
        print(f"Error: The .pages file {file_path} is not a valid ZIP file.")
    except Exception as e:
        print(f"Error extracting text from .pages file {file_path}: {e}")
    finally:
        # Clean up the extracted directory
        if os.path.isdir(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except OSError as e:
                print(f"Error: Could not delete temp directory {temp_dir}. Reason: {e}")

    return text if text_content else ""

# Function to scan .pages files for the specifications
def scan_pages(file_path, specs):
    found_specs = []
    try:
        text = extract_text_from_pages(file_path)  # Extract the text from the .pages file
        
        if isinstance(text, str):  # Ensure the extracted text is a string
            for spec in specs:
                if re.search(re.escape(spec), text, re.IGNORECASE):
                    found_specs.append(spec)
        else:
            raise TypeError("Extracted content is not a string")
    
    except Exception as e:
        print(f"Error scanning .pages file {file_path}: {e}")
    
    return found_specs
# Function to scan all documents in the folder for the specifications
def scan_documents(folder_path, specs):
    results = {}
    doc_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf") or f.endswith(".docx") or f.endswith(".md") or f.endswith(".pages")]

    for filename in doc_files:
        file_path = os.path.join(folder_path, filename)
        if filename.endswith(".pdf"):
            found_specs = scan_pdf(file_path, specs)
        elif filename.endswith(".docx"):
            found_specs = scan_word(file_path, specs)
        elif filename.endswith(".md"):
            found_specs = scan_markdown(file_path, specs)
        elif filename.endswith(".pages"):
            found_specs = scan_pages(file_path, specs)
        else:
            continue

        # Store the found specifications in the results dictionary
        results[filename] = found_specs
    return results

# Function to browse and select a folder
def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder)

# Function to browse and select the specification file
def browse_spec_file():
    spec_file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if spec_file:
        spec_file_entry.delete(0, tk.END)
        spec_file_entry.insert(0, spec_file)

# Function to start the document scanning process
def start_scan():
    folder_path = folder_entry.get()
    spec_file = spec_file_entry.get()

    # Validation of the folder and specification file paths
    if not folder_path or not os.path.isdir(folder_path):
        messagebox.showerror("Error", "Please select a valid folder.")
        return

    if not spec_file or not os.path.isfile(spec_file):
        messagebox.showerror("Error", "Please select a valid text file.")
        return

    start_button.config(state=tk.DISABLED)  # Disable the Start button while scanning
    scan_status_label.config(text="Scan has started...")
    result_text.delete(1.0, tk.END)
    progress_bar.grid(row=4, column=0, columnspan=3, padx=10, pady=10)  # Display progress bar
    
    specs = read_specifications(spec_file)  # Read the specifications from the file
    results = scan_documents(folder_path, specs)  # Scan documents and check for specifications

    for doc, found_specs in results.items():
        missing_specs = [spec for spec in specs if spec not in found_specs]
        result_text.insert(tk.END, f"\nDocument: {doc}\n")
        if found_specs:
            result_text.insert(tk.END, "Found the following specifications:\n")
            for spec in found_specs:
                result_text.insert(tk.END, f" - {spec}\n")
        else:
            result_text.insert(tk.END, "No required specifications found.\n")
        
        if missing_specs:
            result_text.insert(tk.END, "Missing the following specifications:\n")
            for spec in missing_specs:
                result_text.insert(tk.END, f" - {spec}\n")
        else:
            result_text.insert(tk.END, "All specifications found.\n")

    progress_bar.grid_forget()  # Hide the progress bar when scanning is complete
    scan_status_label.config(text="Scan completed.")
    start_button.config(state=tk.NORMAL)

# Function to reset the application to its initial state
def restart_application():
    folder_entry.delete(0, tk.END)
    spec_file_entry.delete(0, tk.END)
    result_text.delete(1.0, tk.END)
    progress_var.set(0)
    scan_status_label.config(text="")
    start_button.config(state=tk.NORMAL)

# Function to quit the application
def quit_application():
    root.quit()

# Initialize paths if the 'FolderToBeChecked' and 'specifications.txt' already exist
def initialize_paths():
    workspace = os.getcwd()
    folder_path = os.path.join(workspace, 'FolderToBeChecked')
    spec_file_path = os.path.join(workspace, 'specifications.txt')

    if os.path.isdir(folder_path):
        folder_entry.insert(0, folder_path)
        messagebox.showinfo("Folder Auto-Selected", f"Folder 'FolderToBeChecked' found and auto-selected. You can change it if needed.")

    if os.path.isfile(spec_file_path):
        spec_file_entry.insert(0, spec_file_path)
        messagebox.showinfo("Specification File Auto-Selected", f"File 'specifications.txt' found and auto-selected. You can change it if needed.")

# Main application window creation using Tkinter
root = tk.Tk()
root.title("Syllabus Component Scanner")

# Create and arrange the GUI elements (labels, input fields, buttons)
folder_label = tk.Label(root, text="Folder containing documents:")
folder_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
folder_entry = tk.Entry(root, width=50)
folder_entry.grid(row=0, column=1, padx=10, pady=5)
browse_folder_button = tk.Button(root, text="Browse", command=browse_folder)
browse_folder_button.grid(row=0, column=2, padx=10, pady=5)

spec_file_label = tk.Label(root, text="Text file with required components:")
spec_file_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
spec_file_entry = tk.Entry(root, width=50)
spec_file_entry.grid(row=1, column=1, padx=10, pady=5)
browse_spec_file_button = tk.Button(root, text="Browse", command=browse_spec_file)
browse_spec_file_button.grid(row=1, column=2, padx=10, pady=5)

start_button = tk.Button(root, text="Start Scan", command=start_scan)
start_button.grid(row=2, column=0, columnspan=3, padx=10, pady=20)

restart_button = tk.Button(root, text="Restart", command=restart_application)
restart_button.grid(row=3, column=0, padx=10, pady=5, sticky="e")

quit_button = tk.Button(root, text="Quit", command=quit_application)
quit_button.grid(row=3, column=2, padx=10, pady=5, sticky="w")

scan_status_label = tk.Label(root, text="")
scan_status_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

# Progress bar setup
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", variable=progress_var)

# Text area for displaying results
result_text = scrolledtext.ScrolledText(root, width=80, height=20)
result_text.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

initialize_paths()  # Check for pre-existing folder and specification file
root.mainloop()
