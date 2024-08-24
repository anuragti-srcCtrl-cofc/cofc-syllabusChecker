
# Syllabus Component Scanner
<img width="817" alt="Screen Shot 2024-08-24 at 3 38 18 PM" src="https://github.com/user-attachments/assets/4b0de144-b54e-4319-8cf4-eeeb33f7634f">

## Warning

Content and Project generated with help from watsonx.ai and GPT-4
## Overview

This Python tool provides a simple GUI to scan a folder of PDF and Word documents for specific syllabus components, as defined in a separate text file. The tool allows users to select a folder containing documents and a text file with the required syllabus components, then scans the documents to verify if they contain the specified components.

## Features

- Supports PDF and Word (`.docx`) documents
- Allows the user to select a folder and a text file through a graphical user interface (GUI)
- Displays results showing which documents contain the required syllabus components

## Requirements

This tool uses the following Python libraries:

- `PyMuPDF` (`fitz`): For PDF processing
- `python-docx`: For Word document processing
- `tkinter`: For the graphical user interface (part of the standard library in Python)

You can install the required packages using `pip`.

## Installation

1. Make sure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).

2. Clone or download this repository.

3. Install the required Python packages by running the following command in your terminal or command prompt:

   ```bash
   pip install pymupdf python-docx tk
   ```

## Usage

1. Run the `SyllabusCheckerv2.py` script (Uses PyPDF). Or the `SyllabusChecker.py` script (Uses PyMuPDF).

   ```bash
   python SyllabusCheckerv2.py
   ```

2. A graphical window will open.

3. **Select Folder**: Use the "Browse" button to select the folder containing the documents you want to scan (markdown, PDF and `.docx` files). IF a folder called `FolderToBeChecked` already exists in the workspace, it will be auto selected. 

4. **Select Specification File**: Use the "Browse" button to select the text file that contains the required syllabus components (one component per line). IF a file called `specifications.txt` already exists in the workspace, it will be auto selected. 

5. Click the **Start Scan** button to begin scanning.

6. The results will be displayed in the window, indicating which documents contain the specified components.

## Example

1. **Text File (specifications.txt)**:

   ```
   Course Overview
   Learning Outcomes
   Grading Policy
   Attendance Policy
   Course Schedule
   ```

2. **Documents**: Place your `.pdf` and `.docx` syllabus files in a folder.

3. **Running the Tool**: After selecting the folder and the specification file, click "Start Scan". The tool will display the results, showing which components are present in each document.

4. **Tool Information**: This tool has not evolved enough to to check fancy pdf or pages files.. Yet. The tool was made by a game developer so the format of the documents to be checked must be followed to the letter if this tool is to work. The author's own syllabus files did not work because it had tables. The only pdf that does work is one made with a LaTeX editor - exported with universal pdf compatibility (PDF/UA - ISO14289 Specifications). The author has not managed to make the tool work with PDF/UA-2 and WTPDF standards that were released in early 2024.

## Author

- **Anurag Tiwari**
- Email: [tiwaria@cofc.edu](mailto:tiwaria@cofc.edu)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
