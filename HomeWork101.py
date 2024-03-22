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

        self.load_database()
        self.create_widgets()

    def load_database(self):
        try:
            with open(INPUT_FILE, 'r') as file:
                self.data = json.load(file)
                self.current_index = 0
        except FileNotFoundError:
            messagebox.showerror("Error", f"Input file '{INPUT_FILE}' not found.")
            self.root.destroy()

    def create_widgets(self):
        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(padx=10, pady=10)

        self.search_label = tk.Label(self.search_frame, text="Search by Identifier:")
        self.search_label.grid(row=0, column=0, sticky="w")

        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.grid(row=0, column=1, padx=5)

        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_record)
        self.search_button.grid(row=0, column=2, padx=5)

        self.identifier_label = tk.Label(self.root, text="Identifier:")
        self.identifier_label.pack(pady=(0, 5))

        self.identifier_value = tk.Label(self.root, text="")
        self.identifier_value.pack()

        self.identifier_image_label = tk.Label(self.root, text="Identifier Image:")
        self.identifier_image_label.pack()

        self.identifier_image = tk.Label(self.root)
        self.identifier_image.pack()

        self.results_label = tk.Label(self.root, text="Results:")
        self.results_label.pack(pady=(10, 5))

        self.results_value = tk.Label(self.root, text="")
        self.results_value.pack()

        self.result_image_label = tk.Label(self.root, text="Result Image:")
        self.result_image_label.pack()

        self.result_image = tk.Label(self.root)
        self.result_image.pack()

        self.confirmed_identifier_label = tk.Label(self.root, text="Confirmed Identifier:")
        self.confirmed_identifier_label.pack(pady=(10, 5))

        self.confirmed_identifier_entry = tk.Entry(self.root)
        self.confirmed_identifier_entry.pack()

        self.confirmed_results_label = tk.Label(self.root, text="Confirmed Results:")
        self.confirmed_results_label.pack(pady=(10, 5))

        self.confirmed_results_entry = tk.Entry(self.root)
        self.confirmed_results_entry.pack()

        self.update_button = tk.Button(self.root, text="Update", command=self.update_record)
        self.update_button.pack(pady=10)

        self.navigation_frame = tk.Frame(self.root)
        self.navigation_frame.pack(pady=10)

        self.previous_button = tk.Button(self.navigation_frame, text="Previous Record", command=self.previous_record)
        self.previous_button.pack(side="left", padx=(0, 10))

        self.next_button = tk.Button(self.navigation_frame, text="Next Record", command=self.next_record)
        self.next_button.pack(side="left")

        self.save_button = tk.Button(self.root, text="Save Database", command=self.save_database)
        self.save_button.pack(pady=10)

        self.update_fields()

    def display_image(self, label, image_path):
        try:
            image = tk.PhotoImage(file=image_path)
            label.config(image=image)
            label.image = image
        except tk.TclError as e:
            messagebox.showerror("Error", f"Failed to load image: {image_path}\nError: {str(e)}")

    def search_record(self):
        identifier = self.search_entry.get()
        if identifier:
            for idx, record in enumerate(self.data):
                if record["identifier"] == identifier:
                    self.current_index = idx
                    self.update_fields()
                    return
            messagebox.showinfo("Info", f"No record found with identifier '{identifier}'.")

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
        if self.data:
            record = self.data[self.current_index]
            self.identifier_value.config(text=record["identifier"])

            # Displaying identifier image
            if "identifier_image" in record:
                identifier_image_path = record["identifier_image"]
                self.display_image(self.identifier_image, identifier_image_path)

            self.results_value.config(text=", ".join(map(str, record["results"])))

            # Displaying result image
            if "result_image" in record:
                result_image_path = record["result_image"]
                self.display_image(self.result_image, result_image_path)

            self.confirmed_identifier_entry.delete(0, tk.END)
            self.confirmed_identifier_entry.insert(0, record.get("confirmed_identifier", ""))
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
