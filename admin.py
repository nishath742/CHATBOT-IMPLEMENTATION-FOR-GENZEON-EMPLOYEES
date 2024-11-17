import tkinter as tk
from tkinter import ttk
import sqlite3

def fetch_user_details():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT username, created_at, last_login FROM users")
    users = c.fetchall()
    conn.close()
    return users

def show_admin_panel():
    # Create main window
    root = tk.Tk()
    root.title("Admin Panel")
    root.geometry("600x400")

    # Fetch user details
    users = fetch_user_details()

    # Create treeview for displaying user details
    columns = ('Username', 'Created At', 'Last Login')
    tree = ttk.Treeview(root, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    for user in users:
        tree.insert('', tk.END, values=user)

    tree.pack(expand=True, fill='both')

    root.mainloop()

if __name__ == "__main__":
    show_admin_panel()
