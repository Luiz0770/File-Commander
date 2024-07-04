import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess

class FileBrowserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Browser")
        self.files = []
        self.current_index = -1
        self.folder_path = ""
        self.destination_folder1 = ""
        self.destination_folder2 = ""

        self.label = tk.Label(root, text="Selecione uma pasta")
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="Selecionar Pasta", command=self.select_folder)
        self.select_button.pack(pady=10)

        self.file_label = tk.Label(root, text="", cursor="hand2")
        self.file_label.pack(pady=10)
        self.file_label.bind("<Button-1>", self.copy_filename_to_clipboard)

        self.move_button1 = tk.Button(root, text="Mover para Pasta 1", command=self.move_file_to_folder1)
        self.move_button1.pack(pady=10)

        self.move_button2 = tk.Button(root, text="Mover para Pasta 2", command=self.move_file_to_folder2)
        self.move_button2.pack(pady=10)

        self.open_button = tk.Button(root, text="Abrir Arquivo", command=self.open_file_or_folder)
        self.open_button.pack(pady=10)

        self.prev_button = tk.Button(root, text="Anterior", command=self.show_prev_file, state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT, padx=20, pady=10)

        self.next_button = tk.Button(root, text="Próximo", command=self.show_next_file, state=tk.DISABLED)
        self.next_button.pack(side=tk.RIGHT, padx=20, pady=10)

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.files = sorted(os.listdir(self.folder_path))
            self.current_index = 0
            self.update_file_label()
            self.update_buttons()

    def update_file_label(self):
        if self.files:
            self.file_label.config(text=self.files[self.current_index])
            self.move_button1.config(state=tk.NORMAL)
            self.move_button2.config(state=tk.NORMAL)
            self.open_button.config(state=tk.NORMAL)
        else:
            self.file_label.config(text="")
            self.move_button1.config(state=tk.DISABLED)
            self.move_button2.config(state=tk.DISABLED)
            self.open_button.config(state=tk.DISABLED)

    def update_buttons(self):
        if self.current_index > 0:
            self.prev_button.config(state=tk.NORMAL)
        else:
            self.prev_button.config(state=tk.DISABLED)

        if self.current_index < len(self.files) - 1:
            self.next_button.config(state=tk.NORMAL)
        else:
            self.next_button.config(state=tk.DISABLED)

    def show_prev_file(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_file_label()
            self.update_buttons()

    def show_next_file(self):
        if self.current_index < len(self.files) - 1:
            self.current_index += 1
            self.update_file_label()
            self.update_buttons()

    def copy_filename_to_clipboard(self, event):
        filename = self.file_label.cget("text")
        self.root.clipboard_clear()
        self.root.clipboard_append(filename)
        messagebox.showinfo("Copiado", f"Nome do arquivo '{filename}' copiado para a área de transferência!")

    def move_file_to_folder1(self):
        if not self.destination_folder1:
            self.destination_folder1 = filedialog.askdirectory(title="Selecione a pasta de destino para o botão 1")
            if not self.destination_folder1:
                messagebox.showerror("Erro", "Pasta de destino para o botão 1 não selecionada!")
                return

        current_file = self.files[self.current_index]
        source_path = os.path.join(self.folder_path, current_file)
        destination_path = os.path.join(self.destination_folder1, current_file)
        try:
            shutil.move(source_path, destination_path)
            messagebox.showinfo("Sucesso", f"Arquivo '{current_file}' movido para '{self.destination_folder1}'")
            self.files.pop(self.current_index)
            if self.current_index >= len(self.files):
                self.current_index = len(self.files) - 1
            self.update_file_label()
            self.update_buttons()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível mover o arquivo para o botão 1: {e}")

    def move_file_to_folder2(self):
        if not self.destination_folder2:
            self.destination_folder2 = filedialog.askdirectory(title="Selecione a pasta de destino para o botão 2")
            if not self.destination_folder2:
                messagebox.showerror("Erro", "Pasta de destino para o botão 2 não selecionada!")
                return

        current_file = self.files[self.current_index]
        source_path = os.path.join(self.folder_path, current_file)
        destination_path = os.path.join(self.destination_folder2, current_file)
        try:
            shutil.move(source_path, destination_path)
            messagebox.showinfo("Sucesso", f"Arquivo '{current_file}' movido para '{self.destination_folder2}'")
            self.files.pop(self.current_index)
            if self.current_index >= len(self.files):
                self.current_index = len(self.files) - 1
            self.update_file_label()
            self.update_buttons()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível mover o arquivo para o botão 2: {e}")

    def open_file_or_folder(self):
        if not self.files:
            return

        selected_item = self.files[self.current_index]
        selected_item_path = os.path.join(self.folder_path, selected_item)

        if os.path.isfile(selected_item_path):
            if os.name == 'nt':  # Windows
                os.startfile(selected_item_path)
            else:  # Linux and macOS
                subprocess.Popen(['xdg-open', selected_item_path])
        elif os.path.isdir(selected_item_path):
            files_in_folder = os.listdir(selected_item_path)
            if files_in_folder:
                first_file = files_in_folder[0]
                first_file_path = os.path.join(selected_item_path, first_file)
                if os.name == 'nt':  # Windows
                    os.startfile(first_file_path)
                else:  # Linux and macOS
                    subprocess.Popen(['xdg-open', first_file_path])
            else:
                messagebox.showwarning("Aviso", f"A pasta '{selected_item}' está vazia!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileBrowserApp(root)
    root.mainloop()
