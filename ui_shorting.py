import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import shutil
import webbrowser


file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg", ".ico", ".heic", ".jfif", ".raw", ".psd"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv", ".mpeg", ".mpg", ".3gp", ".webm", ".m4v", ".vob", ".ogv"],
    "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".odt", ".ods", ".odp", ".rtf", ".tex", ".csv", ".tsv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".alac", ".aiff", ".amr"],
    "Other/Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso"],
    "Other/Scripts": [".py", ".js", ".html", ".css", ".php", ".java", ".cpp", ".c", ".h", ".sh", ".bat", ".ts"],
    "Other/Executables": [".exe", ".msi", ".apk", ".dmg", ".bin", ".run"],
    "Other/Fonts": [".ttf", ".otf", ".woff", ".woff2", ".eot"],
    "Other/Design Files": [".ai", ".indd", ".eps", ".xd", ".fig", ".sketch"],
}




def count_files_by_type(base_path):
    file_counts = {key: 0 for key in file_types.keys()}
    other_files = 0

    for root, _, files in os.walk(base_path):
        for file_name in files:
            file_extension = os.path.splitext(file_name)[1].lower()
            categorized = False
            for category, extensions in file_types.items():
                if file_extension in extensions:
                    file_counts[category] += 1
                    categorized = True
                    break
            if not categorized:
                other_files += 1

    return file_counts, other_files


def organize_files():
    folder_path = folder_path_var.get()

    if not folder_path or not os.path.exists(folder_path):
        messagebox.showwarning("Invalid Path", "Please select a valid folder.")
        return

    
    for category in file_types.keys():
        category_folder = os.path.join(folder_path, category)
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)

    
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_extension = os.path.splitext(file_name)[1].lower()
            for category, extensions in file_types.items():
                if file_extension in extensions:
                    source = os.path.join(root, file_name)
                    destination = os.path.join(folder_path, category, file_name)
                    try:
                        shutil.move(source, destination)
                    except Exception as e:
                        print(f"Error moving file {file_name}: {e}")
                    break

    messagebox.showinfo("Organize Files", "Files have been organized successfully.")


def update_progress_bar(progress_frame, counts, total_files):
    for widget in progress_frame.winfo_children():
        widget.destroy()

    if total_files == 0:
        return

    colors = {
        "Images": "#58BD58",
        "Videos": "#5C5CEA",
        "Documents": "#A838A8",
        "Audio": "#F8B844",
        "Other": "#403F3F",
    }

    bar_frame = tk.Frame(progress_frame, height=6)  
    bar_frame.pack(fill=tk.X, pady=5, padx=10)
    total_width = progress_frame.winfo_width() * 0.95
    for category, count in counts.items():
        if count > 0:
            width = (count / total_files) * total_width
            bar = tk.Frame(bar_frame, bg=colors[category], width=int(width), height=6)
            bar.pack(side=tk.LEFT, fill=tk.Y)

    label_frame = tk.Frame(progress_frame)
    label_frame.pack(fill=tk.X, pady=5, padx=10)  
    
    for category, count in counts.items():
        if total_files > 0:
            percentage = round((count / total_files) * 100)
            
            
            item_frame = tk.Frame(label_frame, bg="#ffffff", padx=0)  
            item_frame.pack(side=tk.LEFT, padx=0)  

            
            square = tk.Frame(item_frame, width=8, height=8, bg=colors[category])
            square.pack(side=tk.LEFT, padx=1, pady=2)

            
            label = tk.Label(item_frame, text=f"{category} ({percentage}%)", font=("Arial", 7), bg="#ffffff")
            label.pack(side=tk.LEFT)


def on_path_update(*args):
    folder_path = folder_path_var.get()
    
    
    if not folder_path or not os.path.exists(folder_path):
        reset_progress()
        return

    file_counts, other_files = count_files_by_type(folder_path)
    total_files = sum(file_counts.values()) + other_files
    counts = {**file_counts, "Other": other_files}
    update_progress_bar(progress_frame, counts, total_files)


def reset_progress():
    folder_path_var.set("")
    for widget in progress_frame.winfo_children():
        widget.destroy()
    progress_frame.pack_forget()  


def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_path_var.set(folder_path)


def create_drop_shadow(frame, x_offset=0, y_offset=0, blur_radius=5, shadow_color="#000000", opacity=0.25):
    shadow = tk.Frame(frame, bg=shadow_color)
    shadow.place(relwidth=1, relheight=1, relx=x_offset, rely=y_offset)
    shadow.config(bg=shadow_color)



root = tk.Tk()
root.title("Clearspace")
root.geometry("450x600")
root.resizable(False, False)


root.iconbitmap(r"C:\Users\Deepu Kashyap\Desktop\shorting python script\images\png\flower.ico")


root.configure(bg="#F3F9FE")


outer_container = tk.Frame(root, bg="#F3F9FE")
outer_container.pack(fill=tk.BOTH, padx=10, pady=10)


create_drop_shadow(outer_container, x_offset=2, y_offset=2, blur_radius=10, shadow_color="#000000", opacity=0.5)

image_container = tk.Frame(outer_container, bg="#F3F9FE")
image_container.pack(fill=tk.X, pady=5, padx=5)


image_path = r"C:\Users\Deepu Kashyap\Desktop\shorting python script\images\png\banner2.png"


img = Image.open(image_path)
img = img.resize((450, 150), Image.LANCZOS)
img_tk = ImageTk.PhotoImage(img)


img_label = tk.Label(image_container, image=img_tk, bg="#F3F9FE")
img_label.pack()


elements_container = tk.Frame(outer_container, bg="#ffffff", relief=tk.RAISED, height=300)
elements_container.pack(fill=tk.BOTH, padx=5, pady=5)


create_drop_shadow(elements_container, x_offset=4, y_offset=4, blur_radius=5, shadow_color="#000000", opacity=0.25)


tk.Label(elements_container, text="Master Folder Path:", font=("Segoe UI Variable", 11), bg="#ffffff", anchor="w").pack(fill=tk.X, padx=(20, 30), pady=(20, 15))  # Added margin here

folder_path_var = tk.StringVar()


entry_frame = tk.Frame(elements_container, bg="#ffffff")
entry_frame.pack(fill=tk.X, pady=(0, 2))  


input_field = tk.Entry(
    entry_frame,
    textvariable=folder_path_var,
    font=("Segoe UI Historic", 8),
    bg="#F5F5F5",  
    fg="#9B9B9B", 
    relief="flat",
    highlightbackground="#9B9B9B",  
    highlightthickness=1,  
)
input_field.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=20, ipady=6) 


button_frame = tk.Frame(elements_container, bg="#ffffff")
button_frame.pack(fill=tk.X, pady=15, padx=25)

browse_button = tk.Button(
    button_frame,
    text="Browse Folder",
    font=("Segoe UI", 10),
    bg="#494949",
    fg="#ffffff",
    relief=tk.RAISED,
    width=15,
    height=1,
    bd=0,
    highlightthickness=0,
    command=browse_folder
    
)
browse_button.pack(side=tk.LEFT, padx=(160, 10))

organize_button = tk.Button(
    button_frame,
    text="Organize Files",
    font=("Segoe UI", 10),
    bg="#005FB8",
    fg="#ffffff",
    relief=tk.RAISED,
    width=15,
    height=1,
    bd=0,
    highlightthickness=0,
    command=organize_files
)
organize_button.pack(side=tk.LEFT)


progress_frame = tk.Frame(elements_container, bg="#ffffff")
progress_frame.pack(fill=tk.X, pady=(15, 0), padx=10)

folder_path_var.trace("w", on_path_update)


social_frame = tk.Frame(root, bg="#F3F9FE")
social_frame.pack(side=tk.BOTTOM, pady=30)  


github_icon_path = r"C:\Users\Deepu Kashyap\Desktop\shorting python script\images\png\github.png"  
twitter_icon_path = r"C:\Users\Deepu Kashyap\Desktop\shorting python script\images\png\twitter.png"  
linkedin_icon_path = r"C:\Users\Deepu Kashyap\Desktop\shorting python script\images\png\linkedin.png"  


github_icon = Image.open(github_icon_path).resize((20, 20), Image.LANCZOS)
twitter_icon = Image.open(twitter_icon_path).resize((20, 20), Image.LANCZOS)
linkedin_icon = Image.open(linkedin_icon_path).resize((20, 20), Image.LANCZOS)


github_icon_tk = ImageTk.PhotoImage(github_icon)
twitter_icon_tk = ImageTk.PhotoImage(twitter_icon)
linkedin_icon_tk = ImageTk.PhotoImage(linkedin_icon)


def open_github():
    webbrowser.open("https://github.com/DeepanshuK2002/CleanSpace")

def open_twitter():
    webbrowser.open("https://x.com/Deepanshuk2002")

def open_linkedin():
    webbrowser.open("https://www.linkedin.com/in/deepanshuk2002/")


github_button = tk.Button(social_frame, image=github_icon_tk, bg="#F3F9FE", bd=0, relief="flat", command=open_github)
github_button.pack(side=tk.LEFT, padx=10)


twitter_button = tk.Button(social_frame, image=twitter_icon_tk, bg="#F3F9FE", bd=0, relief="flat", command=open_twitter)
twitter_button.pack(side=tk.LEFT, padx=10)


linkedin_button = tk.Button(social_frame, image=linkedin_icon_tk, bg="#F3F9FE", bd=0, relief="flat", command=open_linkedin)
linkedin_button.pack(side=tk.LEFT, padx=10)


footer_frame = tk.Frame(root, bg="#F3F9FE")
footer_frame.pack(fill=tk.X, pady=10)

footer_label = tk.Label(
    footer_frame,
    text="Clearspace by Deepanshu © 2024",
    font=("Segoe UI Variable", 8),
    bg="#F3F9FE",
    fg="#777777"
)
footer_label.pack()


root.mainloop()