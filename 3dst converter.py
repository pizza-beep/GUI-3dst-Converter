import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from py3dst import Texture3dst
import mimetypes

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
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found! Please select a valid file.")
    except IOError:
        messagebox.showerror("Error", "Cannot read/write the file. Ensure it's not in use.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def select_file():
    file_path = filedialog.askopenfilename(
        title="Select File",
        filetypes=(
            ("Image and 3DST Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.3dst"),
            ("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff"),
            ("3DST Files", "*.3dst"),
            ("All Files", "*.*"),
        )
    )
    if file_path:
        input_path_var.set(file_path)
        show_image(file_path)

def save_output_file():
    file_path = filedialog.asksaveasfilename(
        title="Save Output File",
        defaultextension=".*",
        filetypes=(
            ("PNG Files", "*.png"),
            ("JPEG Files", "*.jpg"),
            ("BMP Files", "*.bmp"),
            ("TIFF Files", "*.tiff"),
            ("3DST Files", "*.3dst"),
            ("All Files", "*.*"),
        )
    )
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
        img_preview = ImageTk.PhotoImage(image)
        
        image_label.config(image=img_preview)
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
        mode_button.config(text="Switch to Convert Image to 3DST")
        input_label.config(text="Select 3DST File:")
    else:
        mode_var.set("image_to_3dst")
        mode_button.config(text="Switch to Convert 3DST to Image")
        input_label.config(text="Select Image File:")

app = tk.Tk()
app.title("3DST and Image Converter")
app.geometry("600x500")

mode_var = tk.StringVar(value="image_to_3dst")
mode_button = tk.Button(app, text="Switch to Convert 3DST to Image", command=toggle_mode, bg="blue", fg="white")
mode_button.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

input_label = tk.Label(app, text="Select Image File:")
input_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

input_path_var = tk.StringVar()
input_entry = tk.Entry(app, textvariable=input_path_var, width=50)
input_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
browse_button = tk.Button(app, text="Browse", command=select_file)
browse_button.grid(row=1, column=2, padx=10, pady=10)

output_path_var = tk.StringVar()
output_entry = tk.Entry(app, textvariable=output_path_var, width=50)
output_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
save_button = tk.Button(app, text="Save As", command=save_output_file)
save_button.grid(row=2, column=2, padx=10, pady=10)

image_label = tk.Label(app, text="Image preview will appear here", bg="gray", width=50, height=25)
image_label.grid(row=3, column=0, columnspan=3, padx=10, pady=20)

convert_button = tk.Button(app, text="Convert", command=convert_file, bg="green", fg="white")
convert_button.grid(row=4, column=1, pady=10)

app.mainloop()
