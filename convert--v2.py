import os
import shutil
import tkinter as tk
from tkinter import messagebox, Listbox,filedialog

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
    messagebox.showinfo("加载成功", "成功加载文件。")

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

    # 刪除名為 '678.pdf' 的文件
    pdf_file_path = os.path.join(folder_path, "678.pdf")
    if os.path.exists(pdf_file_path):
        os.remove(pdf_file_path)


def find_and_process_folder(base_path, target_name):
    for root, dirs, files in os.walk(base_path):
        if root.endswith(target_name):
            process_folder(root)
            return True
    return False


def select_folder():
    target_folder_name = "123"  # 目標資料夾名稱
    base_folder_path = filedialog.askdirectory()
    if base_folder_path:
        if find_and_process_folder(base_folder_path, target_folder_name):
            messagebox.showinfo("完成", "轉換完成。")
        else:
            messagebox.showinfo(
                "警告", "未找到名為 {} 的資料夾。".format(target_folder_name)
            )
    else:
        messagebox.showwarning("警告", "未選擇任何資料夾。")


def update_listbox():
    listbox_files.delete(0, tk.END)
    for file in uploaded_files_styles:
        listbox_files.insert(tk.END, f"Styles: {os.path.basename(file)}")
    for file in uploaded_file_images:
        listbox_files.insert(tk.END, f"Images: {os.path.basename(file)}")


# 创建主窗口
root = tk.Tk()
root.title("EPUB FolderConvert v.02")
root.geometry("400x300")

# 文件列表显示框
listbox_files = Listbox(root, height=6)
listbox_files.pack(pady=10, fill=tk.X)

btn_select_folder = tk.Button(root, text="選擇待處理的資料夾", command=select_folder)
btn_select_folder.pack(pady=10)

# 加载文件并更新列表
load_files()

# 运行主循环
root.mainloop()

