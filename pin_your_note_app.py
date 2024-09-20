import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

class Note:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def to_dict(self):
        return {"title": self.title, "content": self.content}

class PinYourNoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pin Your Note")
        self.notes = []
        self.notes_frame = tk.Frame(root)
        self.notes_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button to Create New Note
        self.create_button = tk.Button(root, text="Create Note", command=self.create_note)
        self.create_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Button to Save Notes
        self.save_button = tk.Button(root, text="Save Notes", command=self.save_notes)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Button to Load Notes
        self.load_button = tk.Button(root, text="Load Notes", command=self.load_notes)
        self.load_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Button to Clear All Notes
        self.clear_button = tk.Button(root, text="Clear All Notes", command=self.clear_all_notes)
        self.clear_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.display_notes()

    def create_note(self):
        title = simpledialog.askstring("Note Title", "Enter the title of the note:")
        if not title:
            return
        content = simpledialog.askstring("Note Content", "Enter the content of the note:")
        if not content:
            return
        note = Note(title, content)
        self.notes.append(note)
        self.display_notes()

    def display_notes(self):
        # Clear the current notes
        for widget in self.notes_frame.winfo_children():
            widget.destroy()
        
        # Display each note
        for note in self.notes:
            note_frame = tk.Frame(self.notes_frame, borderwidth=2, relief="solid", padx=5, pady=5)
            note_frame.pack(fill=tk.X, pady=5, padx=5)

            title_label = tk.Label(note_frame, text=note.title, font=("Helvetica", 16, "bold"))
            title_label.pack(anchor=tk.W)

            content_label = tk.Label(note_frame, text=note.content, wraplength=400)
            content_label.pack(anchor=tk.W)
            
            # Edit Button
            edit_button = tk.Button(note_frame, text="Edit", command=lambda n=note: self.edit_note(n))
            edit_button.pack(side=tk.LEFT, padx=5)

            # Delete Button
            delete_button = tk.Button(note_frame, text="Delete", command=lambda n=note: self.delete_note(n))
            delete_button.pack(side=tk.RIGHT, padx=5)
        
        self.root.update()

    def edit_note(self, note):
        new_content = simpledialog.askstring("Edit Note", "Edit the content of the note:", initialvalue=note.content)
        if new_content is not None:
            note.content = new_content
            self.display_notes()

    def delete_note(self, note):
        if messagebox.askyesno("Delete Note", "Are you sure you want to delete this note?"):
            self.notes.remove(note)
            self.display_notes()

    def save_notes(self):
        with open("notes.json", "w") as file:
            json.dump([note.to_dict() for note in self.notes], file)
        messagebox.showinfo("Save Notes", "Notes saved successfully.")

    def load_notes(self):
        if os.path.exists("notes.json"):
            with open("notes.json", "r") as file:
                notes_data = json.load(file)
                self.notes = [Note(**note) for note in notes_data]
            self.display_notes()
        else:
            self.notes = []
            self.display_notes()

    def clear_all_notes(self):
        if messagebox.askyesno("Clear All Notes", "Are you sure you want to clear all notes?"):
            self.notes = []
            self.display_notes()

if __name__ == "__main__":
    root = tk.Tk()
    app = PinYourNoteApp(root)
    root.mainloop()
