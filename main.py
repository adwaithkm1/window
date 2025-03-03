import requests
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Listbox, Scrollbar

# Server URL
SERVER_URL = "http://localhost:3000"
USERNAME = "admin"  # Change this as needed
PASSWORD = "akm2009"   # Change this as needed

def authenticate():
    global user_authenticated
    username = simpledialog.askstring("Login", "Enter Username:")
    password = simpledialog.askstring("Login", "Enter Password:", show='*')
    
    if username == USERNAME and password == PASSWORD:
        user_authenticated = True
        messagebox.showinfo("Success", "Login successful!")
    else:
        messagebox.showerror("Error", "Invalid username or password!")

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
        messagebox.showerror("Error", "Failed to upload file!")

def list_files():
    response = requests.get(f"{SERVER_URL}/files")
    if response.status_code == 200:
        file_list.delete(0, tk.END)
        files = response.json().get("files", [])
        for file in files:
            file_list.insert(tk.END, file)
    else:
        messagebox.showerror("Error", "Failed to fetch file list!")

def download_file():
    if not user_authenticated:
        authenticate()
        if not user_authenticated:
            return
    
    selected_file = file_list.get(tk.ACTIVE)
    if not selected_file:
        messagebox.showwarning("Warning", "Please select a file to download!")
        return
    
    response = requests.get(f"{SERVER_URL}/uploads/{selected_file}")
    if response.status_code == 200:
        save_path = filedialog.asksaveasfilename(defaultextension="", initialfile=selected_file)
        if save_path:
            with open(save_path, "wb") as file:
                file.write(response.content)
            messagebox.showinfo("Success", "File downloaded successfully!")
    else:
        messagebox.showerror("Error", "Failed to download file!")

def delete_file():
    if not user_authenticated:
        authenticate()
        if not user_authenticated:
            return
    
    selected_file = file_list.get(tk.ACTIVE)
    if not selected_file:
        messagebox.showwarning("Warning", "Please select a file to delete!")
        return
    
    response = requests.delete(f"{SERVER_URL}/delete/{selected_file}")
    if response.status_code == 200:
        messagebox.showinfo("Success", "File deleted successfully!")
        list_files()
    else:
        messagebox.showerror("Error", "Failed to delete file!")

# GUI Setup
root = tk.Tk()
root.title("Secure File Manager")
user_authenticated = False

upload_btn = tk.Button(root, text="Upload File", command=upload_file, width=20)
upload_btn.pack(pady=5)

file_list = Listbox(root, width=50, height=10)
file_list.pack(pady=5)

scrollbar = Scrollbar(root, orient="vertical", command=file_list.yview)
scrollbar.pack(side="right", fill="y")
file_list.config(yscrollcommand=scrollbar.set)

download_btn = tk.Button(root, text="Download File", command=download_file, width=20)
download_btn.pack(pady=5)

delete_btn = tk.Button(root, text="Delete File", command=delete_file, width=20)
delete_btn.pack(pady=5)

list_files()

root.mainloop()
