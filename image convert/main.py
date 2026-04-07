import os
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image

# Supported formats
OUTPUT_FORMATS = ["jpg", "png", "webp", "bmp", "gif", "tiff", "ico"]

# ------------------ Functions ------------------ #
def center_window(root, width=600, height=600):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

def select_images():
    files = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.tif *.webp *.ico")]
    )
    if files:
        listbox.delete(0, END)
        for f in files:
            listbox.insert(END, f)
        progress_label.config(text=f"Selected {len(files)} images")

def select_output_folder():
    folder = filedialog.askdirectory(title="Select Output Folder")
    if folder:
        output_folder_var.set(folder)

def convert_images():
    images = listbox.get(0, END)
    output_format = format_var.get().lower()
    try:
        scale = int(scale_var.get())
        quality = int(quality_var.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Scale and Quality must be numbers.")
        return
    output_folder = output_folder_var.get()

    if not images:
        messagebox.showwarning("No Images", "Please select images first.")
        return
    if not output_folder:
        messagebox.showwarning("No Output Folder", "Please select an output folder.")
        return

    total_images = len(images)
    progress['maximum'] = total_images
    progress['value'] = 0

    for index, img_path in enumerate(images, start=1):
        try:
            img = Image.open(img_path)

            # Resize if scale less than 100%
            if scale < 100:
                new_width = int(img.width * scale / 100)
                new_height = int(img.height * scale / 100)
                img = img.resize((new_width, new_height), Image.ANTIALIAS)

            img_name = os.path.basename(img_path)
            pure_name = os.path.splitext(img_name)[0]
            output_file = os.path.join(output_folder, f"{pure_name}.{output_format}")

            # Format-specific save handling
            if output_format in ["jpg", "jpeg"]:
                if img.mode in ("RGBA", "LA", "P"):
                    img = img.convert("RGB")
                img.save(output_file, "JPEG", quality=quality)
            elif output_format in ["png", "webp", "tiff"]:
                img.save(output_file, output_format.upper(), quality=quality)
            elif output_format == "gif":
                if img.mode not in ("P", "L"):
                    img = img.convert("P", palette=Image.ADAPTIVE)
                img.save(output_file, "GIF")
            elif output_format == "bmp":
                if img.mode in ("RGBA", "LA"):
                    img = img.convert("RGB")
                img.save(output_file, "BMP")
            elif output_format == "ico":
                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGBA")
                img.save(output_file, "ICO")

        except Exception as e:
            messagebox.showerror("Error", f"Error processing {img_path}:\n{str(e)}")

        progress['value'] = index
        percent = int((index / total_images) * 100)
        progress_label.config(text=f"Processing: {index}/{total_images} ({percent}%)")
        root.update_idletasks()

    messagebox.showinfo("Done", "All images converted successfully!")
    progress_label.config(text=f"Completed {total_images}/{total_images} (100%)")

# ------------------ GUI ------------------ #
root = Tk()
root.title("Ceyri Image Converter")

# Optional: set window icon
try:
    root.iconbitmap("app.ico")
except:
    pass

window_width = 600
window_height = 650
center_window(root, window_width, window_height)
root.resizable(False, False)

# Widgets
Button(root, text="Select Images", command=select_images).pack(pady=5)

listbox = Listbox(root, width=70, height=10)
listbox.pack(padx=10, pady=10)

output_folder_var = StringVar()
Button(root, text="Select Output Folder", command=select_output_folder).pack(pady=5)
Entry(root, textvariable=output_folder_var, width=60).pack()

Label(root, text="Select Output Format").pack(pady=(10, 0))
format_var = StringVar(value="jpg")
OptionMenu(root, format_var, *OUTPUT_FORMATS).pack()

Label(root, text="Resize Scale (%)").pack(pady=(10, 0))
scale_var = StringVar(value="100")
Scale(root, from_=10, to=100, orient=HORIZONTAL, variable=scale_var).pack()

Label(root, text="Quality (1 - 100)").pack(pady=(10, 0))
quality_var = StringVar(value="95")
Scale(root, from_=10, to=100, orient=HORIZONTAL, variable=quality_var).pack()

Button(root, text="Convert Images", command=convert_images, bg="green", fg="white").pack(pady=20)

progress = ttk.Progressbar(root, orient=HORIZONTAL, length=400, mode='determinate')
progress.pack(pady=(5, 0))

progress_label = Label(root, text="No images selected")
progress_label.pack(pady=(5, 10))

root.mainloop()
