# 整理資料夾.py
import os
import shutil
import tkinter as tk
from tkinter import messagebox, Listbox, filedialog
import zipfile

# 全局變量，儲存上傳文件路徑
uploaded_files_styles = []
uploaded_file_images = []

def load_files():
    global uploaded_files_styles, uploaded_file_images

    # 加载 ./css/ 文件夹中的所有文件
    css_folder = './css/'
    if os.path.exists(css_folder):
        uploaded_files_styles = [
            os.path.join(css_folder, f) for f in os.listdir(css_folder) if os.path.isfile(os.path.join(css_folder, f))
        ]
    
    # 加载 ./img/ 文件夹中的所有文件
    img_folder = './img/'
    if os.path.exists(img_folder):
        uploaded_file_images = [
            os.path.join(img_folder, f) for f in os.listdir(img_folder) if os.path.isfile(os.path.join(img_folder, f))
        ]
    
    update_listbox()

def copy_folder(src, dst):
    if os.path.exists(src):
        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                copy_folder(s, d)
            else:
                shutil.copy2(s, d)

def unzip_file(file_path, extract_to):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def process_folder(folder_path):
    # 定義資料夾名稱
    css_new_name = "Styles"
    image_new_name = "Images"
    text_folder_name = "Text"

    # 確保目標資料夾存在，重新命名
    css_folder_path = os.path.join(folder_path, "css")
    if os.path.exists(css_folder_path):
        os.rename(css_folder_path, os.path.join(folder_path, css_new_name))
    styles_path = os.path.join(folder_path, css_new_name)  # 定義 styles_path
    if not os.path.exists(styles_path):
        os.makedirs(styles_path)

    image_folder_path = os.path.join(folder_path, "image")
    if os.path.exists(image_folder_path):
        os.rename(image_folder_path, os.path.join(folder_path, image_new_name))
    images_path = os.path.join(folder_path, image_new_name)  # 定義 images_path
    if not os.path.exists(images_path):
        os.makedirs(images_path)

    # 刪除名為 'cover.xhtml' 的文件
    delete_file_path = os.path.join(folder_path, "cover.xhtml")
    if os.path.exists(delete_file_path):
        os.remove(delete_file_path)

    # 刪除名為 'toc.xhtml' 的文件
    delete_file_path = os.path.join(folder_path, "toc.xhtml")
    if os.path.exists(delete_file_path):
        os.remove(delete_file_path)
        
    # 刪除名為 'font' 的資料夾
    font_folder_path = os.path.join(folder_path, "font")
    if os.path.exists(font_folder_path):
        shutil.rmtree(font_folder_path)

    # 新增 Text 資料夾
    text_folder_path = os.path.join(folder_path, text_folder_name)
    if not os.path.exists(text_folder_path):
        os.makedirs(text_folder_path)

    # 移動 Styles 文件
    for file_path in uploaded_files_styles:
        shutil.copy(file_path, styles_path)
        listbox_files.insert(tk.END, f"Styles: {os.path.basename(file_path)}")

    # 移動 Images 文件
    for file_path in uploaded_file_images:
        shutil.copy(file_path, images_path)
        listbox_files.insert(tk.END, f"Images: {os.path.basename(file_path)}")

    # 移動 .xhtml 文件到 Text 資料夾
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".xhtml"):
            shutil.move(
                os.path.join(folder_path, file_name),
                os.path.join(text_folder_path, file_name),
            )
    
    # 複製 ./Misc 資料夾到處理目標資料夾
    misc_src_folder = './Misc'
    misc_dst_folder = os.path.join(folder_path, 'Misc')
    copy_folder(misc_src_folder, misc_dst_folder)

def find_and_process_folder(base_path, target_name):
    for root, dirs, files in os.walk(base_path):
        if root.endswith(target_name):
            process_folder(root)
            return True
    return False

def select_files():
    target_folder_name = "OEBPS"  # 目標資料夾名稱
    file_paths = filedialog.askopenfilenames(filetypes=[("EPUB files", "*.epub"), ("Zip files", "*.zip"), ("All files", "*.*")])
    if file_paths:
        success_files = []
        failure_files = []
        for file_path in file_paths:
            extract_to = os.path.dirname(file_path)  # 解壓縮到選擇文件的同一目錄
            extracted_folder_name = os.path.splitext(os.path.basename(file_path))[0]
            extracted_folder_path = os.path.join(extract_to, extracted_folder_name)
            unzip_file(file_path, extracted_folder_path)
            if find_and_process_folder(extracted_folder_path, target_folder_name):
                success_files.append(file_path)
            else:
                failure_files.append(file_path)

        # 提示轉換結果
        if success_files:
            messagebox.showinfo("完成", f"轉換完成: {', '.join(success_files)}")
        if failure_files:
            messagebox.showinfo("警告", f"未找到名為 {target_folder_name} 的資料夾: {', '.join(failure_files)}")
    else:
        messagebox.showwarning("警告", "未選擇任何壓縮檔案。")

def update_listbox():
    listbox_files.delete(0, tk.END)
    for file in uploaded_files_styles:
        listbox_files.insert(tk.END, f"Styles: {os.path.basename(file)}")
    for file in uploaded_file_images:
        listbox_files.insert(tk.END, f"Images: {os.path.basename(file)}")

# 创建主窗口
root = tk.Tk()
root.title("EPUB 資料夾轉換 v.03")
root.geometry("400x300")

# 文件列表显示框
listbox_files = Listbox(root, height=6)
listbox_files.pack(pady=10, fill=tk.X)

btn_select_files = tk.Button(root, text="選擇待處理的檔案", command=select_files)
btn_select_files.pack(pady=10)

# 加载文件并更新列表
load_files()

# 运行主循环
root.mainloop()
