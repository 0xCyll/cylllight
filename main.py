import tkinter as tk
from tkinter import ttk
from pynput import keyboard
import requests
import mss
import os
import webbrowser
import datetime
import json


upload_url = "https://api.nightlight.gg/v1/upload"
fonte = "Helvetica"
screenshot_folder = os.path.join(os.path.expanduser("~"), "Documents", "cylllight")

os.makedirs(screenshot_folder, exist_ok=True)

window = tk.Tk()
window.title("Cylllight")
window.configure(bg="black")
icon_path = "Path2icon.ico"  # put your own path for the icon
window.iconbitmap(icon_path)
style = ttk.Style()
style.theme_use("clam")
style.configure(".", background="black", foreground="white")
style.configure("TLabel", background="black", foreground="white")
style.configure("TEntry", fieldbackground="white", foreground="black")
style.configure("TButton", font=(fonte, 12), background="darkblue", foreground="white")

trigger_label = ttk.Label(window, text="Trigger Key:")
trigger_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

trigger_entry = ttk.Entry(window, width=10)
trigger_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

def update_trigger_key():
    new_key = trigger_entry.get()
    trigger_label.config(text=f"Trigger Key: {new_key}")

update_button = ttk.Button(window, text="Update", command=update_trigger_key)
update_button.grid(row=0, column=2, padx=10, pady=10, sticky=tk.W)

url_frame = ttk.Frame(window)
url_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=tk.W+tk.E+tk.N+tk.S)
url_scrollbar = ttk.Scrollbar(url_frame)
url_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
url_listbox = tk.Listbox(url_frame, height=10, yscrollcommand=url_scrollbar.set)
url_listbox.pack(fill=tk.BOTH, expand=True)
url_scrollbar.config(command=url_listbox.yview)

def open_selected_url():
    selected_index = url_listbox.curselection()
    if selected_index:
        url = url_listbox.get(selected_index[0])
        webbrowser.open(url)
        url_listbox.itemconfig(selected_index[0], bg="white", fg="black")  

open_button = ttk.Button(window, text="Open URL", command=open_selected_url)
open_button.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

def show_screenshot_folder():
    os.startfile(screenshot_folder)

folder_button = ttk.Button(window, text="Show Folder", command=show_screenshot_folder)
folder_button.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

def remove_selected_url():
    selected_index = url_listbox.curselection()
    if selected_index:
        url_listbox.delete(selected_index[0])

remove_button = ttk.Button(window, text="Remove URL", command=remove_selected_url)
remove_button.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)

class MessageDialog(tk.Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x100")
        self.resizable(False, False)
        label = ttk.Label(self, text=message, font=(fonte, 12))
        label.pack(padx=20, pady=20)
        ok_button = ttk.Button(self, text="OK", command=self.destroy)
        ok_button.pack(pady=10)

def configure_api_key():
    config_file_path = os.path.join(screenshot_folder, "config.json")
    if os.path.exists(config_file_path):
        with open(config_file_path, "r") as config_file:
            config = json.load(config_file)
            api_key = config.get("api_key")
    else:
        api_key = None

    dialog = tk.Toplevel(window)
    dialog.title("API Key Configuration")

    def save_api_key():
        nonlocal api_key
        api_key = api_key_entry.get().strip()
        with open(config_file_path, "w") as config_file:
            json.dump({"api_key": api_key}, config_file)
        dialog.destroy()

    def show_api_key():
        MessageDialog(dialog, "API Key", f"Your current API key is: {api_key}")

    dialog_label = ttk.Label(dialog, text="Please enter your API key:")
    dialog_label.pack(padx=20, pady=20)

    api_key_entry = ttk.Entry(dialog, width=30)
    api_key_entry.pack(padx=20)
    if api_key:
        api_key_entry.insert(tk.END, api_key)

    save_button = ttk.Button(dialog, text="Save", command=save_api_key)
    save_button.pack(pady=10)

    show_button = ttk.Button(dialog, text="Show API Key", command=show_api_key)
    show_button.pack(pady=10)

def take_screenshot_and_upload():
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{current_time}_1.jpg"
    screenshot_file = os.path.join(screenshot_folder, filename)
    with mss.mss() as sct:
        sct.shot(output=screenshot_file)

    config_file_path = os.path.join(screenshot_folder, "config.json")
    if not os.path.exists(config_file_path):
        configure_api_key()
        return

    with open(screenshot_file, "rb") as file:
        with open(config_file_path, "r") as config_file:
            config = json.load(config_file)
            api_key = config.get("api_key")

        response = requests.post(
            upload_url,
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": file}
        )

    if response.status_code == 200:
        response_label.config(text="Screenshot uploaded successfully!")
        response_data = response.json().get("data", {})
        url = response_data.get("url")
        if url:
            url_label.config(text=f"URL: {url}")
            url_listbox.insert(0, url)  
            url_listbox.itemconfig(0, bg="green", fg="white")  
    else:
        response_label.config(text="Upload failed!")
        error_label.config(text=f"Error: {response.json().get('error', {}).get('message')}")

response_label = ttk.Label(window, text="")
response_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

url_label = ttk.Label(window, text="")
url_label.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)

error_label = ttk.Label(window, text="")
error_label.grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)

def on_key_press(key):
    try:
        if key.char == trigger_entry.get():
            take_screenshot_and_upload()
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_key_press)
listener.start()

configure_button = ttk.Button(window, text="Configure API Key", command=configure_api_key)
configure_button.grid(row=6, column=0, padx=10, pady=10, sticky=tk.W)

window.mainloop()
