import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


app = ctk.CTk()
app.title("Agirucltural Crop Trait NER GUI")
app.geometry("1024x768")


selected_dataset = tk.StringVar()
status_text = tk.StringVar(value="Status: Idle")


BASE_DIR = os.path.abspath(".")
TEST_DIR = os.path.join(BASE_DIR, "custom_data", "test")
PRED_DIR = os.path.join(BASE_DIR, "custom_data", "predictions")
BIOC_DIR = os.path.join(BASE_DIR, "custom_data", "bioc")

os.makedirs(TEST_DIR, exist_ok=True)
os.makedirs(PRED_DIR, exist_ok=True)
os.makedirs(BIOC_DIR, exist_ok=True)



def load_dataset():
    folder = filedialog.askdirectory(title="Select Test Dataset Folder")
    
    if not folder or not os.path.isdir(folder):
        status_text.set(" Invalid folder selected.")
        return

    name = os.path.basename(folder.rstrip("/\\"))
    dest = os.path.join(TEST_DIR, name)

    try:
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(folder, dest)
        selected_dataset.set(name)
        status_text.set(f" Dataset '{name}' loaded successfully.")
        dataset_label.configure(text=f"Loaded Dataset: {name}")
    except Exception as e:
        status_text.set(f" Failed to load dataset: {e}")
        selected_dataset.set("")
        dataset_label.configure(text="Loaded Dataset: None")


def run_prediction():
    dataset = selected_dataset.get()
    if not dataset:
        messagebox.showwarning("No dataset", "Please load a dataset first.")
        return

    input_dir = os.path.join(TEST_DIR, dataset)
    output_dir = os.path.join(PRED_DIR, dataset)

    status_text.set("Running prediction...")
    app.update_idletasks()

    try:
        subprocess.run([
            "python", "predict_batch.py",
            "--input_dir", input_dir,
            "--output_dir", output_dir,
            "--dataset_name", "Allcrops"
        ], check=True)
        status_text.set(f"Prediction complete for '{dataset}'.")
    except subprocess.CalledProcessError:
        status_text.set("Prediction failed. Check console.")

def run_bioc_conversion():
    dataset = selected_dataset.get()
    if not dataset:
        messagebox.showwarning("No dataset", "Please load a dataset first.")
        return

    input_dir = os.path.join(PRED_DIR, dataset)
    output_dir = os.path.join(BIOC_DIR, dataset)

    status_text.set(" Converting to BioC...")
    app.update_idletasks()

    try:
        subprocess.run([
            "python", "convert_to_bioc.py",
            "--input_dir", input_dir,
            "--output_dir", output_dir,
            "--source", dataset
        ], check=True)
        status_text.set(f"BioC files created for '{dataset}'.")
    except subprocess.CalledProcessError:
        status_text.set("BioC conversion failed. Check console.")

def reset_all():
    selected_dataset.set("")
    status_text.set("Reset complete.")
    #Remove leftover folder 
    shutil.rmtree(TEST_DIR); os.makedirs(TEST_DIR)
    shutil.rmtree(PRED_DIR); os.makedirs(PRED_DIR)
    shutil.rmtree(BIOC_DIR); os.makedirs(BIOC_DIR)

def quit_app():
    app.destroy()

# UI

# Title
title = ctk.CTkLabel(app, text=" Agricultural Crop Traits", font=ctk.CTkFont(size=24, weight="bold"))
title.pack(pady=20)

# Show current dataset
dataset_label = ctk.CTkLabel(app, text="Loaded Dataset: None", font=ctk.CTkFont(size=16))
dataset_label.pack(pady=10)

load_btn = ctk.CTkButton(app, text="Load Test Dataset", command=load_dataset, width=300)
load_btn.pack(pady=10)

predict_btn = ctk.CTkButton(app, text="Predict Traits", command=run_prediction, width=300)
predict_btn.pack(pady=10)

bioc_btn = ctk.CTkButton(app, text="Convert to BioC", command=run_bioc_conversion, width=300)
bioc_btn.pack(pady=10)

reset_btn = ctk.CTkButton(app, text="Reset", command=reset_all, width=300)
reset_btn.pack(pady=10)

exit_btn = ctk.CTkButton(app, text="Exit", command=quit_app, fg_color="red", hover_color="#8B0000", width=300)
exit_btn.pack(pady=10)

status_label = ctk.CTkLabel(app, textvariable=status_text, font=ctk.CTkFont(size=14))
status_label.pack(pady=20)


app.mainloop()
