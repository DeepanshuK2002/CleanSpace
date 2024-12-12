import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import webbrowser

# File type categories
file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg", ".ico", ".heic", ".jfif", ".raw", ".psd"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv", ".mpeg", ".mpg", ".3gp", ".webm", ".m4v", ".vob", ".ogv"],
    "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".odt", ".ods", ".odp", ".rtf", ".tex", ".csv", ".tsv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".alac", ".aiff", ".amr"],
}

# Count files by type
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

# Update progress bar with proportions
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

    bar_frame = tk.Frame(progress_frame, height=6)  # Height set to 6 for progress bar
    bar_frame.pack(fill=tk.X, pady=5, padx=10)
    total_width = progress_frame.winfo_width() * 0.95
    for category, count in counts.items():
        if count > 0:
            width = (count / total_files) * total_width
            bar = tk.Frame(bar_frame, bg=colors[category], width=int(width), height=6)
            bar.pack(side=tk.LEFT, fill=tk.Y)

    label_frame = tk.Frame(progress_frame)
    label_frame.pack(fill=tk.X, pady=5, padx=10)  # Added padding around label
    
    for category, count in counts.items():
        if total_files > 0:
            percentage = round((count / total_files) * 100)
            
            # Create a frame to hold the small square and the label text with margin
            item_frame = tk.Frame(label_frame, bg="#ffffff", padx=0)  # Added padding (margin) between the square and label
            item_frame.pack(side=tk.LEFT, padx=0)  # Add horizontal padding

            # Create the small square and position it in the frame
            square = tk.Frame(item_frame, width=8, height=8, bg=colors[category])
            square.pack(side=tk.LEFT, padx=1, pady=2)

            # Create the label text and position it next to the square
            label = tk.Label(item_frame, text=f"{category} ({percentage}%)", font=("Arial", 7), bg="#ffffff")
            label.pack(side=tk.LEFT)
            

# Automatically analyze folder path
def on_path_update(*args):
    folder_path = folder_path_var.get()
    
    # Hide the progress bar if the folder path is empty or invalid
    if not folder_path or not os.path.exists(folder_path):
        reset_progress()
        return

    file_counts, other_files = count_files_by_type(folder_path)
    total_files = sum(file_counts.values()) + other_files
    counts = {**file_counts, "Other": other_files}
    update_progress_bar(progress_frame, counts, total_files)

# Reset progress to initial state
def reset_progress():
    folder_path_var.set("")
    for widget in progress_frame.winfo_children():
        widget.destroy()
    progress_frame.pack_forget()  # Hides the progress frame

# Browse folder
def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_path_var.set(folder_path)

# Placeholder for organize button
def organize_files():
    messagebox.showinfo("Organize Files", "File organization functionality goes here.")

# Function to create drop shadow
def create_drop_shadow(frame, x_offset=0, y_offset=0, blur_radius=5, shadow_color="#000000", opacity=0.25):
    shadow = tk.Frame(frame, bg=shadow_color)
    shadow.place(relwidth=1, relheight=1, relx=x_offset, rely=y_offset)
    shadow.config(bg=shadow_color)


# Main GUI
root = tk.Tk()
root.title("Clearspace")
root.geometry("450x600")
root.resizable(False, False)

# Set the icon on the title bar
root.iconbitmap(r"C:\Users\Deepu Kashyap\Desktop\shorting python script\images\png\flower.ico")


# Set the background color for the entire application
root.configure(bg="#F3F9FE")

# Outer container with margin
outer_container = tk.Frame(root, bg="#F3F9FE")
outer_container.pack(fill=tk.BOTH, padx=10, pady=10)

# Create shadow for outer container
create_drop_shadow(outer_container, x_offset=2, y_offset=2, blur_radius=10, shadow_color="#000000", opacity=0.5)

# Image container above the current container
image_container = tk.Frame(outer_container, bg="#F3F9FE")
image_container.pack(fill=tk.X, pady=5, padx=5)

# Absolute path to your image
image_path = r"C:\Users\Deepu Kashyap\Desktop\shorting python script\images\png\banner2.png"

# Open the image using Pillow
img = Image.open(image_path)
img = img.resize((450, 150), Image.LANCZOS)
img_tk = ImageTk.PhotoImage(img)

# Display the image in the Tkinter Label widget
img_label = tk.Label(image_container, image=img_tk, bg="#F3F9FE")
img_label.pack()

# Elements container with different height
elements_container = tk.Frame(outer_container, bg="#ffffff", relief=tk.RAISED, height=300)
elements_container.pack(fill=tk.BOTH, padx=5, pady=5)

# Create shadow for elements container
create_drop_shadow(elements_container, x_offset=4, y_offset=4, blur_radius=5, shadow_color="#000000", opacity=0.25)

# UI elements
tk.Label(elements_container, text="Master Folder Path:", font=("Segoe UI Variable", 11), bg="#ffffff", anchor="w").pack(fill=tk.X, padx=(20, 30), pady=(20, 15))  # Added margin here

folder_path_var = tk.StringVar()

# Frame for input field alignment with added margin
entry_frame = tk.Frame(elements_container, bg="#ffffff")
entry_frame.pack(fill=tk.X, pady=(0, 2))  # Added bottom margin to the input field

# Input field with updated styles
input_field = tk.Entry(
    entry_frame,
    textvariable=folder_path_var,
    font=("Segoe UI Historic", 8),
    bg="#F5F5F5",  # Approximation of #9B9B9B with 30% opacity
    fg="#9B9B9B",  # Text color
    relief="flat",
    highlightbackground="#9B9B9B",  # Border color
    highlightthickness=1,  # Border thickness
)
input_field.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=20, ipady=6)  # ipady increases height

# Browse and Organize Files button frame with margin adjustments
button_frame = tk.Frame(elements_container, bg="#ffffff")
button_frame.pack(fill=tk.X, pady=(20, 20))  # Added top and bottom margin to the button frame

btn_width = 12  # Adjust width as needed
btn_height = 1  # Custom height (fractional values don't work directly, but we approximate)
btn_padding_y = int(btn_height * 4)  # Adjust multiplier to control height

# Organize Files button with custom height approximation
tk.Button(button_frame, text="Organize Files", command=organize_files, font=("Arial", 10), 
          width=btn_width, bg="#005FB8", fg="white", relief="flat", bd=0, 
          highlightthickness=0, pady=btn_padding_y).pack(side=tk.RIGHT, padx=20)

# Browse button with custom height approximation
tk.Button(button_frame, text="Browse", command=browse_folder, font=("Arial", 10), 
          width=btn_width, bg="#9B9B9B", fg="white", relief="flat", bd=0, 
          highlightthickness=0, pady=btn_padding_y).pack(side=tk.LEFT, padx=20)

# Progress bar container
progress_frame = tk.Frame(elements_container, bg="#ffffff", height=30)
progress_frame.pack(fill=tk.X, pady=10)

# Add listener for folder path change
folder_path_var.trace_add("write", on_path_update)

# Social Media Icons section at the bottom of the screen
social_frame = tk.Frame(root, bg="#F3F9FE")
social_frame.pack(side=tk.BOTTOM, pady=30)  # Pack this frame at the bottom of the screen

# Path to your social media icon images
github_icon_path = r"C:\Users\Deepu Kashyap\Desktop\shorting python script\images\png\github.png"  # Path to your GitHub icon
twitter_icon_path = r"C:\Users\Deepu Kashyap\Desktop\shorting python script\images\png\twitter.png"  # Path to your Twitter icon
linkedin_icon_path = r"C:\Users\Deepu Kashyap\Desktop\shorting python script\images\png\linkedin.png"  # Path to your LinkedIn icon

# Load and resize images
github_icon = Image.open(github_icon_path).resize((20, 20), Image.LANCZOS)
twitter_icon = Image.open(twitter_icon_path).resize((20, 20), Image.LANCZOS)
linkedin_icon = Image.open(linkedin_icon_path).resize((20, 20), Image.LANCZOS)

# Convert to Tkinter compatible images
github_icon_tk = ImageTk.PhotoImage(github_icon)
twitter_icon_tk = ImageTk.PhotoImage(twitter_icon)
linkedin_icon_tk = ImageTk.PhotoImage(linkedin_icon)

# Define functions to open social media pages
def open_github():
    webbrowser.open("https://github.com/DeepanshuK2002/CleanSpace")

def open_twitter():
    webbrowser.open("https://x.com/Deepanshuk2002")

def open_linkedin():
    webbrowser.open("https://www.linkedin.com/in/deepanshuk2002/")

# GitHub button with the image
github_button = tk.Button(social_frame, image=github_icon_tk, bg="#F3F9FE", bd=0, relief="flat", command=open_github)
github_button.pack(side=tk.LEFT, padx=10)

# Twitter button with the image
twitter_button = tk.Button(social_frame, image=twitter_icon_tk, bg="#F3F9FE", bd=0, relief="flat", command=open_twitter)
twitter_button.pack(side=tk.LEFT, padx=10)

# LinkedIn button with the image
linkedin_button = tk.Button(social_frame, image=linkedin_icon_tk, bg="#F3F9FE", bd=0, relief="flat", command=open_linkedin)
linkedin_button.pack(side=tk.LEFT, padx=10)


root.mainloop()
