import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import csv

class ModDownloaderUI:
    def __init__(self, root, versions, loaders, on_download_callback=None):
        self.root = root
        self.root.title("Minecraft Mod Auto-Downloader")
        self.root.geometry("600x500")

        self.version_list = versions
        self.loader_list = loaders
        self.on_download_callback = on_download_callback

        self.settings_frame = ttk.LabelFrame(root, text="Settings", padding=(10, 10))
        self.settings_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.mod_name_label = ttk.Label(self.settings_frame, text="Mod Names:")
        self.mod_name_label.grid(row=0, column=0, sticky="w")

        self.mod_name_entry = ttk.Entry(self.settings_frame, width=40)
        self.mod_name_entry.grid(row=0, column=1, padx=(5, 0), sticky="w")

        self.add_mod_button = ttk.Button(self.settings_frame, text="Add Mod", command=self.add_mod_to_list)
        self.add_mod_button.grid(row=0, column=2, padx=(5, 0))

        self.mod_list = tk.Listbox(self.settings_frame, height=5, width=50)
        self.mod_list.grid(row=1, column=0, columnspan=3, pady=(5, 0), sticky="ew")

        self.version_label = ttk.Label(self.settings_frame, text="Minecraft Version:")
        self.version_label.grid(row=2, column=0, sticky="w")

        self.version_var = tk.StringVar()
        self.version_dropdown = ttk.Combobox(self.settings_frame, textvariable=self.version_var, values=self.version_list, width=37)
        self.version_dropdown.grid(row=2, column=1, padx=(5, 0), sticky="w")
        self.version_dropdown.set("Select version")

        self.loader_label = ttk.Label(self.settings_frame, text="Mod Loader:")
        self.loader_label.grid(row=3, column=0, sticky="w")

        self.loader_var = tk.StringVar()
        self.loader_dropdown = ttk.Combobox(self.settings_frame, textvariable=self.loader_var, values=self.loader_list, width=37)
        self.loader_dropdown.grid(row=3, column=1, padx=(5, 0), sticky="w")
        self.loader_dropdown.set("Select loader")

        self.path_label = ttk.Label(self.settings_frame, text="Download Path:")
        self.path_label.grid(row=4, column=0, sticky="w")

        self.path_entry = ttk.Entry(self.settings_frame, width=40)
        self.path_entry.grid(row=4, column=1, padx=(5, 0), sticky="w")

        self.browse_button = ttk.Button(self.settings_frame, text="Browse", command=self.select_download_path)
        self.browse_button.grid(row=4, column=2, padx=(5, 0))

        self.save_button = ttk.Button(self.settings_frame, text="Save Mods to CSV", command=self.save_mods_to_csv)
        self.save_button.grid(row=5, column=1, padx=(5, 0), pady=(5, 0), sticky="w")

        self.load_button = ttk.Button(self.settings_frame, text="Load Mods from CSV", command=self.load_mods_from_csv)
        self.load_button.grid(row=6, column=1, padx=(5, 0), pady=(5, 0), sticky="w")

        self.search_button = ttk.Button(root, text="Start Search & Download", command=self.start_download)
        self.search_button.grid(row=1, column=0, pady=(5, 0), padx=10, sticky="ew")

        self.feedback_frame = ttk.LabelFrame(root, text="Download Status", padding=(10, 10))
        self.feedback_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.status_list = tk.Listbox(self.feedback_frame, height=10, width=60)
        self.status_list.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.feedback_frame, orient="vertical", command=self.status_list.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.status_list.config(yscrollcommand=self.scrollbar.set)

        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)

        self.mod_names = []

    def add_mod_to_list(self):
        mod_name = self.mod_name_entry.get().strip()
        if mod_name:
            self.mod_names.append(mod_name)
            self.mod_list.insert(tk.END, mod_name)
            self.mod_name_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a mod name.")

    def select_download_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)

    def start_download(self):
        if self.on_download_callback:
            download_thread = threading.Thread(target=self.run_download)
            download_thread.start()

    def run_download(self):
        self.on_download_callback(self.get_inputs())

    def update_status(self, message):
        self.root.after(0, self._update_status_list, message)

    def _update_status_list(self, message):
        self.status_list.insert(tk.END, message)
        self.status_list.yview(tk.END)

    def get_inputs(self):
        return {
            "mods": self.mod_names,
            "version": self.version_var.get(),
            "loader": self.loader_var.get(),
            "download_path": self.path_entry.get(),
        }

    def save_mods_to_csv(self):
        if not self.mod_names:
            messagebox.showwarning("No Mods", "No mods to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    for mod in self.mod_names:
                        writer.writerow([mod])
                messagebox.showinfo("Success", "Mods saved to CSV!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save mods to CSV: {str(e)}")

    def load_mods_from_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, mode='r', newline='') as file:
                    reader = csv.reader(file)
                    loaded_mods = [row[0] for row in reader]
                    if loaded_mods:
                        self.mod_names.extend(loaded_mods)
                        self.mod_list.delete(0, tk.END)
                        for mod in self.mod_names:
                            self.mod_list.insert(tk.END, mod)
                        messagebox.showinfo("Success", "Mods loaded from CSV!")
                    else:
                        messagebox.showwarning("No Mods", "The CSV file contains no mod names.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load mods from CSV: {str(e)}")
