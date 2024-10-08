import os
import re
import pypdf
import docx
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

def read_specifications(spec_file):
    with open(spec_file, 'r') as file:
        specs = file.readlines()
    specs = [spec.strip() for spec in specs if spec.strip()]
    return specs

def scan_pdf(file_path, specs):
    found_specs = []
    try:
        reader = pypdf.PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        for spec in specs:
            if re.search(re.escape(spec), text, re.IGNORECASE):
                found_specs.append(spec)
    except Exception as e:
        print(f"Error scanning PDF {file_path}: {e}")
    return found_specs

def scan_word(file_path, specs):
    found_specs = []
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        for spec in specs:
            if re.search(re.escape(spec), text, re.IGNORECASE):
                found_specs.append(spec)
    except Exception as e:
        print(f"Error scanning Word document {file_path}: {e}")
    return found_specs

def scan_markdown(file_path, specs):
    found_specs = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        for spec in specs:
            if re.search(re.escape(spec), text, re.IGNORECASE):
                found_specs.append(spec)
    except Exception as e:
        print(f"Error scanning Markdown {file_path}: {e}")
    return found_specs

def scan_documents(folder_path, specs):
    results = {}
    doc_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf") or f.endswith(".docx") or f.endswith(".md")]

    for filename in doc_files:
        file_path = os.path.join(folder_path, filename)
        if filename.endswith(".pdf"):
            found_specs = scan_pdf(file_path, specs)
        elif filename.endswith(".docx"):
            found_specs = scan_word(file_path, specs)
        elif filename.endswith(".md"):
            found_specs = scan_markdown(file_path, specs)
        else:
            continue

        results[filename] = found_specs
    return results

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder)

def browse_spec_file():
    spec_file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if spec_file:
        spec_file_entry.delete(0, tk.END)
        spec_file_entry.insert(0, spec_file)

def start_scan():
    folder_path = folder_entry.get()
    spec_file = spec_file_entry.get()

    if not folder_path or not os.path.isdir(folder_path):
        messagebox.showerror("Error", "Please select a valid folder.")
        return

    if not spec_file or not os.path.isfile(spec_file):
        messagebox.showerror("Error", "Please select a valid text file.")
        return

    start_button.config(state=tk.DISABLED)
    scan_status_label.config(text="Scan has started...")
    result_text.delete(1.0, tk.END)
    progress_bar.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
    
    specs = read_specifications(spec_file)
    results = scan_documents(folder_path, specs)

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

    progress_bar.grid_forget()
    scan_status_label.config(text="Scan completed.")
    start_button.config(state=tk.NORMAL)

def restart_application():
    # Clear all input fields and reset the progress bar
    folder_entry.delete(0, tk.END)
    spec_file_entry.delete(0, tk.END)
    result_text.delete(1.0, tk.END)
    progress_var.set(0)
    scan_status_label.config(text="")
    start_button.config(state=tk.NORMAL)

def quit_application():
    root.quit()

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

root = tk.Tk()
root.title("Syllabus Component Scanner")

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

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", variable=progress_var)

result_text = scrolledtext.ScrolledText(root, width=80, height=20)
result_text.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

initialize_paths()
root.mainloop()
