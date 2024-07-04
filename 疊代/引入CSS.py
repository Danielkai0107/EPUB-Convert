# 引入CSS.py
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re

def find_oebps_folder(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if 'OEBPS' in dirnames:
            return os.path.join(dirpath, 'OEBPS')
    return None

def find_xhtml_files(oebps_folder):
    xhtml_files = []
    for dirpath, dirnames, filenames in os.walk(oebps_folder):
        for filename in filenames:
            if filename.endswith('.xhtml'):
                xhtml_files.append(os.path.join(dirpath, filename))
    return xhtml_files

def insert_css_to_xhtml(xhtml_files, styles_folder):
    css_files = [f for f in os.listdir(styles_folder) if f.endswith('.css')]
    css_links = ''.join([f'<link rel="stylesheet" href="../Styles/{css_file}" />\n' for css_file in css_files])
    head_pattern = re.compile(r'(</head>)', re.IGNORECASE)

    for xhtml_file in xhtml_files:
        with open(xhtml_file, 'r', encoding='utf-8') as file:
            content = file.read()

        new_content = head_pattern.sub(css_links + r'\1', content, count=1)
        
        with open(xhtml_file, 'w', encoding='utf-8') as file:
            file.write(new_content)

def main():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Select Folder")
    
    if folder_selected:
        oebps_folder = find_oebps_folder(folder_selected)
        if oebps_folder:
            styles_folder = os.path.join(oebps_folder, 'Styles')
            if os.path.exists(styles_folder):
                xhtml_files = find_xhtml_files(oebps_folder)
                if xhtml_files:
                    insert_css_to_xhtml(xhtml_files, styles_folder)
                    messagebox.showinfo("Success", "CSS files have been successfully inserted into XHTML files.")
                else:
                    messagebox.showwarning("Warning", "No XHTML files found in the OEBPS folder.")
            else:
                messagebox.showwarning("Warning", "Styles folder not found in the OEBPS folder.")
        else:
            messagebox.showwarning("Warning", "OEBPS folder not found in the selected directory.")
    else:
        messagebox.showwarning("Warning", "No folder selected.")

if __name__ == "__main__":
    main()
