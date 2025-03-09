import requests
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar

# Server URL
SERVER_URL = "http://localhost:5000"  # Make sure this matches your Flask server


def upload_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    
    with open(file_path, "rb") as file:
        response = requests.post(f"{SERVER_URL}/upload", files={"file": file})
    
    if response.status_code == 200:
        messagebox.showinfo("Success", "File uploaded successfully!")
        list_files()
    else:
        messagebox.showerror("Error", f"Upload failed! ({response.status_code})")


def list_files():
    response = requests.get(f"{SERVER_URL}/files")
    if response.status_code == 200:
        file_list.delete(0, tk.END)
        files = response.json().get("files", [])
        if not files:
            file_list.insert(tk.END, "No files available.")
        else:
            for file in files:
                file_list.insert(tk.END, file)
    else:
        messagebox.showerror("Error", "Failed to fetch file list!")


def download_file():
    selected_file = file_list.get(tk.ACTIVE)
    if not selected_file or selected_file == "No files available.":
        messagebox.showwarning("Warning", "Select a valid file to download!")
        return
    
    response = requests.get(f"{SERVER_URL}/download/{selected_file}")
    if response.status_code == 200:
        save_path = filedialog.asksaveasfilename(defaultextension="", initialfile=selected_file)
        if save_path:
            with open(save_path, "wb") as file:
                file.write(response.content)
            messagebox.showinfo("Success", "File downloaded successfully!")
    else:
        messagebox.showerror("Error", f"Download failed! ({response.status_code})")


def delete_file():
    selected_file = file_list.get(tk.ACTIVE)
    if not selected_file or selected_file == "No files available.":
        messagebox.showwarning("Warning", "Select a valid file to delete!")
        return
    
    response = requests.delete(f"{SERVER_URL}/delete/{selected_file}")
    if response.status_code == 200:
        messagebox.showinfo("Success", "File deleted successfully!")
        list_files()
    else:
        messagebox.showerror("Error", f"Delete failed! ({response.status_code})")


# GUI Setup
root = tk.Tk()
root.title("Simple File Manager")
root.geometry("400x350")

upload_btn = tk.Button(root, text="Upload File", command=upload_file, width=25)
upload_btn.pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=5)

file_list = Listbox(frame, width=50, height=10)
file_list.pack(side="left", fill="y")

scrollbar = Scrollbar(frame, orient="vertical", command=file_list.yview)
scrollbar.pack(side="right", fill="y")
file_list.config(yscrollcommand=scrollbar.set)

download_btn = tk.Button(root, text="Download File", command=download_file, width=25)
download_btn.pack(pady=5)

delete_btn = tk.Button(root, text="Delete File", command=delete_file, width=25)
delete_btn.pack(pady=5)

list_files()

root.mainloop()
