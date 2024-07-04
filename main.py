import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re

def find_OEBPS_folder(starting_folder):
    for root, dirs, files in os.walk(starting_folder):
        if 'OEBPS' in dirs:
            return os.path.join(root, 'OEBPS')
    return None

def correct_image_paths(file_path, images_folder):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    img_tags = re.findall(r'<img[^>]+src="([^"]+)"', content)
    for img_src in img_tags:
        img_name = os.path.basename(img_src)
        relative_images_folder = os.path.relpath(images_folder, os.path.dirname(file_path))
        corrected_img_src = os.path.join(relative_images_folder, img_name).replace('\\', '/')
        if img_src != corrected_img_src:
            content = content.replace(img_src, corrected_img_src)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def rename_images_in_html(file_path, images_folder, img_rename_map):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    img_tags = re.findall(r'<img[^>]+src="([^"]+)"', content)
    img_counter = len(img_rename_map)  # 確保編號從前次基數繼續

    for img_src in img_tags:
        img_name = os.path.basename(img_src)
        img_ext = os.path.splitext(img_name)[1]
        old_img_path = os.path.join(images_folder, img_name)

        if any('\u4e00' <= char <= '\u9fff' for char in img_src):
            if img_src not in img_rename_map:
                new_img_name = f'ch-{img_counter}{img_ext}'
                new_img_path = os.path.join(images_folder, new_img_name)
                
                if os.path.exists(old_img_path):
                    os.rename(old_img_path, new_img_path)
                
                relative_images_folder = os.path.relpath(images_folder, os.path.dirname(file_path))
                new_img_src = os.path.join(relative_images_folder, new_img_name).replace('\\', '/')
                img_rename_map[img_src] = new_img_src
                img_counter += 1
            else:
                new_img_src = img_rename_map[img_src]
            content = content.replace(img_src, new_img_src)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def find_xhtml_files(oebps_folder):
    xhtml_files = []
    for dirpath, dirnames, filenames in os.walk(oebps_folder):
        for filename in filenames:
            if filename.endswith('.xhtml'):
                xhtml_files.append(os.path.join(dirpath, filename))
    return xhtml_files

def insert_css_and_js_to_xhtml(xhtml_files, styles_folder, scripts_folder):
    css_files = [f for f in os.listdir(styles_folder) if f.endswith('.css')]
    css_links = ''.join([f'<link rel="stylesheet" href="../Styles/{css_file}" />\n' for css_file in css_files])
    
    js_files = [f for f in os.listdir(scripts_folder) if f.endswith('.js')]
    js_links = ''.join([f'<script src="../Misc/{js_file}"></script>\n' for js_file in js_files])
    
    head_pattern = re.compile(r'(</head>)', re.IGNORECASE)

    for xhtml_file in xhtml_files:
        with open(xhtml_file, 'r', encoding='utf-8') as file:
            content = file.read()

        new_content = head_pattern.sub(css_links + js_links + r'\1', content, count=1)
        
        with open(xhtml_file, 'w', encoding='utf-8') as file:
            file.write(new_content)

def process_folder(folder_selected):
    obs_folder = find_OEBPS_folder(folder_selected)
    if (obs_folder):
        images_folder = os.path.join(obs_folder, 'Images')

        file_extension = file_type.get()
        html_files = []
        for root, _, files in os.walk(obs_folder):
            for file in files:
                if file.endswith(file_extension):
                    html_files.append(os.path.join(root, file))

        if html_files and os.path.exists(images_folder):
            img_rename_map = {}

            # 先修正所有圖片路徑
            for html_file_path in html_files:
                correct_image_paths(html_file_path, images_folder)

            # 然後進行重命名
            for html_file_path in html_files:
                rename_images_in_html(html_file_path, images_folder, img_rename_map)
            
            # 找到所有 xhtml 文件並插入 CSS 和 JS
            xhtml_files = find_xhtml_files(obs_folder)
            styles_folder = os.path.join(obs_folder, 'Styles')
            scripts_folder = os.path.join(obs_folder, 'Misc')
            if os.path.exists(styles_folder) and os.path.exists(scripts_folder):
                insert_css_and_js_to_xhtml(xhtml_files, styles_folder, scripts_folder)
                return True, f"資料夾 '{folder_selected}' 已處理所有 {file_extension} 文件，並插入 CSS 和 JS 文件。"
            else:
                return False, f"資料夾 '{folder_selected}' 中未找到 Styles 或 Misc 資料夾。"
        else:
            return False, f"資料夾 '{folder_selected}' 結構不正確，請確認 OEBPS 和 Images 資料夾存在。"
    else:
        return False, f"資料夾 '{folder_selected}' 中未找到 OEBPS 資料夾。"

def select_folders():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        subfolders = [os.path.join(folder_selected, subfolder) for subfolder in os.listdir(folder_selected) if os.path.isdir(os.path.join(folder_selected, subfolder))]
        all_successful = True
        messages = []
        for subfolder in subfolders:
            success, message = process_folder(subfolder)
            messages.append(message)
            if not success:
                all_successful = False
        
        if all_successful:
            messagebox.showinfo("成功", "\n".join(messages))
        else:
            messagebox.showerror("錯誤", "\n".join(messages))

# 創建 Tkinter 主窗口
root = tk.Tk()
root.title("圖片重新命名與 CSS 和 JS 插入")
root.geometry("400x200")

# 創建文件類型選擇下拉選單
file_type = tk.StringVar(value=".xhtml")
file_type_label = tk.Label(root, text="選擇要處理的文件類型：")
file_type_label.pack(pady=5)
file_type_option = tk.OptionMenu(root, file_type, ".html", ".xhtml")
file_type_option.pack(pady=5)

# 創建選擇資料夾按鈕
select_button = tk.Button(root, text="選擇資料夾", command=select_folders)
select_button.pack(pady=20)

# 開始 Tkinter 主循環
root.mainloop()
