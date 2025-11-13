import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class FolderViewerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("📁 Folder Content Viewer")
        self.geometry("800x600")
        self.resizable(True, True)

        # 使用 ttk 主题
        style = ttk.Style()
        style.theme_use('clam')  # 更现代的主题：'clam', 'alt', 'default'
        style.configure(".", font=("Helvetica", 11))
        style.configure("TLabel", background="#f0f0f0")
        style.configure("Header.TLabel", font=("Helvetica", 16, "bold"))

        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Header
        header = ttk.Label(self, text="📁 Folder Content Viewer", style="Header.TLabel")
        header.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        subtitle = ttk.Label(
            self,
            text="Enter folder path or browse to select a file.",
            foreground="gray"
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 10))

        # Input frame
        input_frame = ttk.Frame(self)
        input_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        input_frame.columnconfigure(0, weight=1)

        self.path_var = tk.StringVar()
        path_entry = ttk.Entry(input_frame, textvariable=self.path_var, font=("Helvetica", 12))
        path_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        browse_btn = ttk.Button(input_frame, text="📂 Browse File", command=self.browse_file)
        browse_btn.grid(row=0, column=1, padx=(0, 10))

        load_btn = ttk.Button(input_frame, text="🔍 Load Folder", command=self.load_folder)
        load_btn.grid(row=0, column=2)

        # Result
        result_label = ttk.Label(self, text="Files in Folder:")
        result_label.grid(row=3, column=0, padx=20, pady=(10, 5), sticky="w")

        self.textbox = tk.Text(
            self,
            font=("Courier", 10),
            wrap="none",
            bg="#f9f9f9",
            fg="#333"
        )
        v_scroll = ttk.Scrollbar(self, orient="vertical", command=self.textbox.yview)
        h_scroll = ttk.Scrollbar(self, orient="horizontal", command=self.textbox.xview)
        self.textbox.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.textbox.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="nsew")
        v_scroll.grid(row=4, column=1, pady=(0, 20), sticky="ns")
        h_scroll.grid(row=5, column=0, padx=20, sticky="ew")

        # Initial focus
        self.path_var.set("")

    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Select a File")
        if file_path:
            folder_path = os.path.dirname(file_path)
            self.path_var.set(folder_path)

    def load_folder(self):
        path = self.path_var.get().strip()
        if not path:
            messagebox.showwarning("Input Required", "Please enter a folder path.")
            return
        if not os.path.exists(path):
            messagebox.showerror("Not Found", f"Path not found:\n{path}")
            return
        if not os.path.isdir(path):
            messagebox.showerror("Invalid", "This is not a folder.")
            return

        try:
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            content = "\n".join(files) if files else "(No files)"
            self.textbox.delete("1.0", tk.END)
            self.textbox.insert("1.0", content)
        except PermissionError:
            messagebox.showerror("Permission Denied", "Cannot access this folder.")

if __name__ == "__main__":
    app = FolderViewerApp()
    app.mainloop()
