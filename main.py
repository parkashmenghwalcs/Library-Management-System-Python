import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ---------------- DATABASE ---------------- #

conn = sqlite3.connect("books.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    year TEXT
)
""")
conn.commit()

# ---------------- FUNCTIONS ---------------- #

def update_count():
    cursor.execute("SELECT COUNT(*) FROM books")
    count = cursor.fetchone()[0]
    count_label.config(text=f"Total Books: {count}")

def add_book():
    title = title_entry.get()
    author = author_entry.get()
    year = year_entry.get()

    if not title or not author or not year:
        messagebox.showerror("Error", "Fill all fields")
        return

    cursor.execute(
        "INSERT INTO books(title, author, year) VALUES(?,?,?)",
        (title, author, year)
    )

    conn.commit()

    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)

    messagebox.showinfo("Success", "Book Added Successfully")

    view_books()
    update_count()

def view_books():

    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM books")

    for book in cursor.fetchall():
        tree.insert("", tk.END, values=book)

def search_book():

    keyword = search_entry.get()

    for row in tree.get_children():
        tree.delete(row)

    cursor.execute(
        "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
        ('%' + keyword + '%', '%' + keyword + '%')
    )

    for book in cursor.fetchall():
        tree.insert("", tk.END, values=book)

def delete_book():

    selected = tree.selection()

    if not selected:
        messagebox.showerror("Error", "Select a Book")
        return

    item = tree.item(selected)

    book_id = item["values"][0]

    cursor.execute(
        "DELETE FROM books WHERE id=?",
        (book_id,)
    )

    conn.commit()

    messagebox.showinfo("Success", "Book Deleted")

    view_books()
    update_count()

# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Library Management System")
root.geometry("1200x700")
root.configure(bg="#2C3E50")

# Header

header = tk.Label(
    root,
    text="📚 Library Management System",
    font=("Arial", 24, "bold"),
    bg="#2C3E50",
    fg="white"
)
header.pack(pady=15)

# Input Frame

input_frame = tk.Frame(root, bg="#34495E")
input_frame.pack(pady=10, padx=10, fill="x")

tk.Label(input_frame, text="Title", bg="#34495E", fg="white").grid(row=0, column=0, padx=10, pady=10)
title_entry = tk.Entry(input_frame, width=25)
title_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Author", bg="#34495E", fg="white").grid(row=0, column=2, padx=10)
author_entry = tk.Entry(input_frame, width=25)
author_entry.grid(row=0, column=3)

tk.Label(input_frame, text="Year", bg="#34495E", fg="white").grid(row=0, column=4, padx=10)
year_entry = tk.Entry(input_frame, width=15)
year_entry.grid(row=0, column=5)

# Buttons

button_frame = tk.Frame(root, bg="#2C3E50")
button_frame.pack(pady=15)

tk.Button(
    button_frame,
    text="➕ Add Book",
    command=add_book,
    bg="#27AE60",
    fg="white",
    font=("Arial", 11, "bold"),
    width=15
).grid(row=0, column=0, padx=10)

tk.Button(
    button_frame,
    text="📖 View Books",
    command=view_books,
    bg="#2980B9",
    fg="white",
    font=("Arial", 11, "bold"),
    width=15
).grid(row=0, column=1, padx=10)

tk.Button(
    button_frame,
    text="🗑 Delete Book",
    command=delete_book,
    bg="#C0392B",
    fg="white",
    font=("Arial", 11, "bold"),
    width=15
).grid(row=0, column=2, padx=10)

# Search Frame

search_frame = tk.Frame(root, bg="#2C3E50")
search_frame.pack()

search_entry = tk.Entry(search_frame, width=40)
search_entry.grid(row=0, column=0, padx=10)

tk.Button(
    search_frame,
    text="🔍 Search",
    command=search_book,
    bg="#F39C12",
    fg="white",
    font=("Arial", 10, "bold")
).grid(row=0, column=1)

# Table

style = ttk.Style()
style.theme_use("clam")

tree = ttk.Treeview(
    root,
    columns=("ID", "Title", "Author", "Year"),
    show="headings",
    height=15
)

tree.heading("ID", text="Book ID")
tree.heading("Title", text="Title")
tree.heading("Author", text="Author")
tree.heading("Year", text="Year")

tree.column("ID", width=80)
tree.column("Title", width=350)
tree.column("Author", width=250)
tree.column("Year", width=120)

tree.pack(fill="both", expand=True, padx=20, pady=20)

# Footer

count_label = tk.Label(
    root,
    text="Total Books: 0",
    font=("Arial", 12, "bold"),
    bg="#2C3E50",
    fg="white"
)
count_label.pack(pady=10)

view_books()
update_count()

root.mainloop()