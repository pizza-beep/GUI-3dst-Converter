import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
from py3dst import Texture3dst
import os

# Load or create options file
def load_options():
    if os.path.exists("options.txt"):
        with open("options.txt", "r") as f:
            return f.read().strip()
    return "dark"

def save_options(theme):
    with open("options.txt", "w") as f:
        f.write(theme)

# Set theme based on options file
current_theme = load_options()
ctk.set_appearance_mode(current_theme)
ctk.set_default_color_theme("blue")

def is_3dst_file(file_path):
    return file_path.lower().endswith(".3dst")

def convert_file_generic(input_path, output_path, mode):
    try:
        if mode == "image_to_3dst":
            image = Image.open(input_path)
            texture = Texture3dst().fromImage(image)
            texture.export(output_path)
        else:
            texture = Texture3dst().open(input_path)
            width, height = texture.size
            image = texture.copy(0, 0, width, height)
            image.save(output_path)
        messagebox.showinfo("Success", f"Successfully converted to: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[
        ("Image and 3DST Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.3dst"),
        ("All Files", "*.*")
    ])
    if file_path:
        input_path_var.set(file_path)
        show_image(file_path)

def save_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".*", filetypes=[
        ("PNG Files", "*.png"),
        ("JPEG Files", "*.jpg"),
        ("3DST Files", "*.3dst"),
        ("All Files", "*.*")
    ])
    if file_path:
        output_path_var.set(file_path)

def show_image(file_path):
    try:
        if is_3dst_file(file_path):
            texture = Texture3dst().open(file_path)
            width, height = texture.size
            image = texture.copy(0, 0, width, height)
        else:
            image = Image.open(file_path)
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
        image.thumbnail((400, 400))
        img_preview = ctk.CTkImage(light_image=image, size=(300, 300))
        image_label.configure(image=img_preview, text="")
        image_label.image = img_preview
    except Exception as e:
        messagebox.showerror("Error", f"Cannot load image: {e}")

def convert_file():
    input_path = input_path_var.get()
    output_path = output_path_var.get()
    if not input_path or not output_path:
        messagebox.showwarning("Warning", "Please select both input and output files!")
        return
    convert_file_generic(input_path, output_path, mode_var.get())

def toggle_mode():
    if mode_var.get() == "image_to_3dst":
        mode_var.set("three_dst_to_image")
        mode_button.configure(text="Switch to Convert Image to 3DST")
        input_label.configure(text="Select 3DST File:")
    else:
        mode_var.set("image_to_3dst")
        mode_button.configure(text="Switch to Convert 3DST to Image")
        input_label.configure(text="Select Image File:")

def change_theme(theme):
    ctk.set_appearance_mode(theme)
    save_options(theme)

app = ctk.CTk()
app.title("3DST Image Converter")
app.geometry("750x650")
app.grid_columnconfigure(1, weight=1)

mode_var = ctk.StringVar(value="image_to_3dst")
mode_button = ctk.CTkButton(app, text="Switch to Convert 3DST to Image", command=toggle_mode, width=200, height=40)
mode_button.grid(row=0, column=1, padx=10, pady=10)

input_label = ctk.CTkLabel(app, text="Select Image File:")
input_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

input_path_var = ctk.StringVar()
input_entry = ctk.CTkEntry(app, textvariable=input_path_var, width=400)
input_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
browse_button = ctk.CTkButton(app, text="Browse", command=select_file, width=100, height=40)
browse_button.grid(row=1, column=2, padx=10, pady=10)

output_path_var = ctk.StringVar()
output_entry = ctk.CTkEntry(app, textvariable=output_path_var, width=400)
output_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
save_button = ctk.CTkButton(app, text="Save As", command=save_output_file, width=100, height=40)
save_button.grid(row=2, column=2, padx=10, pady=10)

image_label = ctk.CTkLabel(app, text="Image preview will appear here", width=300, height=300)
image_label.grid(row=3, column=0, columnspan=3, padx=10, pady=20)

convert_button = ctk.CTkButton(app, text="Convert", command=convert_file, width=200, height=50)
convert_button.grid(row=4, column=1, pady=10)

options_menu = ctk.CTkOptionMenu(app, values=["light", "dark"], command=change_theme, width=150, height=40)
options_menu.set(current_theme)
options_menu.grid(row=5, column=1, pady=10)

app.mainloop()
