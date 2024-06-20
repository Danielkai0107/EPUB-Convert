import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox

# 全局变量，存储上传的文件路径
uploaded_files_styles = []
uploaded_file_images = ""


def process_folder(folder_path):
    # 定义新文件夹名称
    css_new_name = "Styles"
    image_new_name = "Images"
    text_folder_name = "Text"

    # 确保目标文件夹存在，并尝试重命名
    css_folder_path = os.path.join(folder_path, "css")
    if os.path.exists(css_folder_path):
        os.rename(css_folder_path, os.path.join(folder_path, css_new_name))
    styles_path = os.path.join(folder_path, css_new_name)  # 正确定义styles_path
    if not os.path.exists(styles_path):
        os.makedirs(styles_path)

    image_folder_path = os.path.join(folder_path, "image")
    if os.path.exists(image_folder_path):
        os.rename(image_folder_path, os.path.join(folder_path, image_new_name))
    images_path = os.path.join(folder_path, image_new_name)  # 正确定义images_path
    if not os.path.exists(images_path):
        os.makedirs(images_path)

    # 创建 Text 文件夹
    text_folder_path = os.path.join(folder_path, text_folder_name)
    if not os.path.exists(text_folder_path):
        os.makedirs(text_folder_path)

    # 移动 Styles 文件
    for file_path in uploaded_files_styles:
        shutil.copy(file_path, styles_path)
        listbox_files.insert(tk.END, f"Styles: {os.path.basename(file_path)}")

    # 移动 Images 文件
    if uploaded_file_images:
        shutil.copy(uploaded_file_images, images_path)
        listbox_files.insert(
            tk.END, f"Images: {os.path.basename(uploaded_file_images)}"
        )

    # 移动 .xhtml 文件到 Text 文件夹
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".xhtml"):
            shutil.move(
                os.path.join(folder_path, file_name),
                os.path.join(text_folder_path, file_name),
            )

    # 删除名为 '678.pdf' 的文件
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
    target_folder_name = "123"  # 根据实际情况替换为目标文件夹名
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


def upload_files_styles():
    global uploaded_files_styles
    filenames = filedialog.askopenfilenames(
        title="選擇 CSS 文件", filetypes=(("所有文件", "*.*"),)
    )
    if len(filenames) == 3:
        uploaded_files_styles = list(filenames)
        update_listbox()
        messagebox.showinfo("上传成功", "成功上传三个文件。")
    else:
        messagebox.showwarning("错误", "请确保您上传了三个文件。")


def upload_file_images():
    global uploaded_file_images
    filename = filedialog.askopenfilename(
        title="選擇 play.svg", filetypes=(("所有文件", "*.*"),)
    )
    if filename:
        uploaded_file_images = filename
        update_listbox()
        messagebox.showinfo("上傳成功", "成功上傳一個文件。")
    else:
        messagebox.showwarning("錯誤", "上傳失敗，請重新上傳。")


def update_listbox():
    listbox_files.delete(0, tk.END)
    for file in uploaded_files_styles:
        listbox_files.insert(tk.END, f"Styles: {os.path.basename(file)}")
    if uploaded_file_images:
        listbox_files.insert(
            tk.END, f"Images: {os.path.basename(uploaded_file_images)}"
        )


# 创建主窗口
root = tk.Tk()
root.title("EPUB FolderConvert")
root.geometry("400x300")

# 创建并放置按钮
btn_upload_files_styles = tk.Button(
    root, text="上傳 CSS 文件 (選擇3個)", command=upload_files_styles
)
btn_upload_files_styles.pack(pady=10)
btn_upload_file_images = tk.Button(
    root, text="上傳 play.svg (選擇1個)", command=upload_file_images
)
btn_upload_file_images.pack(pady=10)

# 文件列表显示框
listbox_files = Listbox(root, height=6)
listbox_files.pack(pady=10, fill=tk.X)

btn_select_folder = tk.Button(root, text="選擇待處理的資料夾", command=select_folder)
btn_select_folder.pack(pady=10)

# 运行主循环
root.mainloop()
