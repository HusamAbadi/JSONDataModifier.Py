import tkinter as tk
from tkinter import filedialog, messagebox
import json

INPUT_FILE = "Data_Directory/database.json"
OUTPUT_FILE = "Data_Directory/output_data.json"


class DatabaseEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Editor")

        self.data = None
        self.current_index = None

        self.load_button = tk.Button(root, text="Load Database", command=self.load_database)
        self.load_button.pack(pady=10)

        self.identifier_label = tk.Label(root, text="Identifier:")
        self.identifier_label.pack()
        self.identifier_entry = tk.Entry(root)
        self.identifier_entry.pack()

        self.confirmed_identifier_label = tk.Label(root, text="Confirmed Identifier:")
        self.confirmed_identifier_label.pack()
        self.confirmed_identifier_entry = tk.Entry(root)
        self.confirmed_identifier_entry.pack()

        self.results_label = tk.Label(root, text="Results:")
        self.results_label.pack()
        self.results_entry = tk.Entry(root)
        self.results_entry.pack()

        self.confirmed_results_label = tk.Label(root, text="Confirmed Results:")
        self.confirmed_results_label.pack()
        self.confirmed_results_entry = tk.Entry(root)
        self.confirmed_results_entry.pack()

        self.update_button = tk.Button(root, text="Update", command=self.update_record)
        self.update_button.pack(pady=10)

        self.next_button = tk.Button(root, text="Next Record", command=self.next_record)
        self.next_button.pack(pady=5)

        self.previous_button = tk.Button(root, text="Previous Record", command=self.previous_record)
        self.previous_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Save Database", command=self.save_database)
        self.save_button.pack(pady=10)

    def load_database(self):
        try:
            with open(INPUT_FILE, 'r') as file:
                self.data = json.load(file)
                self.current_index = 0
                self.update_fields()
        except FileNotFoundError:
            messagebox.showerror("Error", f"Input file '{INPUT_FILE}' not found.")

    def update_record(self):
        if self.data:
            confirmed_identifier = self.confirmed_identifier_entry.get()
            confirmed_results = self.confirmed_results_entry.get()

            if confirmed_identifier and confirmed_results:
                self.data[self.current_index]["confirmed_identifier"] = confirmed_identifier
                self.data[self.current_index]["confirmed_results"] = [int(x) for x in confirmed_results.split(",")]
                self.update_fields()
                messagebox.showinfo("Success", "Record updated successfully.")
            else:
                messagebox.showerror("Error", "Confirmed Identifier and Confirmed Results cannot be empty.")
        else:
            messagebox.showerror("Error", "No database loaded.")

    def update_fields(self):
        record = self.data[self.current_index]
        self.identifier_entry.delete(0, tk.END)
        self.identifier_entry.insert(0, record["identifier"])
        self.confirmed_identifier_entry.delete(0, tk.END)
        self.confirmed_identifier_entry.insert(0, record.get("confirmed_identifier", ""))
        self.results_entry.delete(0, tk.END)
        self.results_entry.insert(0, ", ".join(map(str, record["results"])))
        self.confirmed_results_entry.delete(0, tk.END)
        self.confirmed_results_entry.insert(0, ", ".join(map(str, record.get("confirmed_results", record["results"]))))

    def next_record(self):
        if self.data and self.current_index < len(self.data) - 1:
            self.current_index += 1
            self.update_fields()

    def previous_record(self):
        if self.data and self.current_index > 0:
            self.current_index -= 1
            self.update_fields()

    def save_database(self):
        if self.data:
            with open(OUTPUT_FILE, 'w') as file:
                json.dump(self.data, file, indent=4)
                messagebox.showinfo("Success", f"Database saved successfully as '{OUTPUT_FILE}'.")
        else:
            messagebox.showerror("Error", "No database loaded.")


if __name__ == "__main__":
    root = tk.Tk()
    editor = DatabaseEditor(root)
    root.mainloop()
