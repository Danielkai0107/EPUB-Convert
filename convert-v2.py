import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, simpledialog

# 全局变量，存储上传的文件路径
uploaded_files_styles = []
uploaded_file_images = ""

# 全局变量，存储用户选择的文件夹路径
selected_folders = []

def process_folder(folder_path):
    # 定义新文件夹名称并确保文件夹存在
    folder_names = {'css': 'Styles', 'image': 'Images', 'text': 'Text'}
    for old, new in folder_names.items():
        old_path = os.path.join(folder_path, old)
        new_path = os.path.join(folder_path, new)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
        if not os.path.exists(new_path):
            os.makedirs(new_path)

    # 处理上传的文件
    styles_path = os.path.join(folder_path, folder_names['css'])
    images_path = os.path.join(folder_path, folder_names['image'])
    text_path = os.path.join(folder_path, folder_names['text'])

    for file_path in uploaded_files_styles:
        shutil.copy(file_path, styles_path)
        listbox_files.insert(tk.END, f"Styles: {os.path.basename(file_path)}")

    if uploaded_file_images:
        shutil.copy(uploaded_file_images, images_path)
        listbox_files.insert(tk.END, f"Images: {os.path.basename(uploaded_file_images)}")

    # 移动 .xhtml 文件到 Text 文件夹
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.xhtml'):
            shutil.move(os.path.join(folder_path, file_name), text_path)

    # 删除名为 '678.pdf' 的文件
    pdf_file_path = os.path.join(folder_path, '678.pdf')
    if os.path.exists(pdf_file_path):
        os.remove(pdf_file_path)

def upload_files_styles():
    global uploaded_files_styles
    filenames = filedialog.askopenfilenames(title="选择三个文件", filetypes=(("所有文件", "*.*"),))
    if len(filenames) == 3:
        uploaded_files_styles = list(filenames)
        update_listbox()
        messagebox.showinfo("上传成功", "成功上传三个文件。")
    else:
        messagebox.showwarning("错误", "请确保您上传了三个文件。")

def upload_file_images():
    global uploaded_file_images
    filename = filedialog.askopenfilename(title="选择一个文件", filetypes=(("所有文件", "*.*"),))
    if filename:
        uploaded_file_images = filename
        update_listbox()
        messagebox.showinfo("上传成功", "成功上传一个文件。")
    else:
        messagebox.showwarning("错误", "上传文件失败，请重试。")

def update_listbox():
    listbox_files.delete(0, tk.END)
    for file in uploaded_files_styles:
        listbox_files.insert(tk.END, f"Styles: {os.path.basename(file)}")
    if uploaded_file_images:
        listbox_files.insert(tk.END, f"Images: {os.path.basename(uploaded_file_images)}")

def batch_process_folders():
    for folder_path in selected_folders:
        if os.path.isdir(folder_path):
            process_folder(folder_path)
    messagebox.showinfo("完成", "所有选中文件夹的批处理任务完成。")
    selected_folders.clear()  # 清空列表以便下次使用

def select_folders():
    folder_path = filedialog.askdirectory()
    if folder_path:
        selected_folders.append(folder_path)
        update_listbox_folders()
    else:
        messagebox.showwarning("警告", "未选择任何文件夹。")

def update_listbox_folders():
    listbox_folders.delete(0, tk.END)
    for folder in selected_folders:
        listbox_folders.insert(tk.END, folder)

# 创建主窗口
root = tk.Tk()
root.title("批处理工具")
root.geometry("400x400")

# 创建并放置按钮
btn_upload_files_styles = tk.Button(root, text="上传Styles文件 (选择三个)", command=upload_files_styles)
btn_upload_files_styles.pack(pady=10)
btn_upload_file_images = tk.Button(root, text="上传Images文件 (选择一个)", command=upload_file_images)
btn_upload_file_images.pack(pady=10)

btn_select_folder = tk.Button(root, text="添加要处理的文件夹", command=select_folders)
btn_select_folder.pack(pady=10)

btn_process_all = tk.Button(root, text="处理所有选中的文件夹", command=batch_process_folders)
btn_process_all.pack(pady=10)

# 文件列表显示框
listbox_files = Listbox(root, height=6)
listbox_files.pack(pady=10, fill=tk.X)

# 文件夹列表显示框
listbox_folders = Listbox(root, height=10)
listbox_folders.pack(pady=10, fill=tk.X)

root.mainloop()
