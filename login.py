import tkinter as tk
import re
from tkinter import messagebox, ttk
import sqlite3
import subprocess
import os

# Database setup
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT
            )''')
c.execute('''CREATE TABLE IF NOT EXISTS admin (
                username TEXT PRIMARY KEY,
                password TEXT
            )''')
conn.commit()

# Function to handle signup
def signup():
    username = entry_signup_username.get()
    password = entry_signup_password.get()

    # Validate email format
    if not re.match(r"[^@]+@genzeon\.com$", username):
        messagebox.showerror("Signup Failed", "Email must be in the format username@genzeon.com")
        return

    if not username or not password:
        messagebox.showerror("Signup Failed", "Username and password cannot be empty.")
        return

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                  (username, password))
        conn.commit()
        messagebox.showinfo("Signup Successful", "You can now log in.")
        show_login_frame()
    except sqlite3.IntegrityError:
        messagebox.showerror("Signup Failed", "Username already exists.")
    except sqlite3.Error as e:
        messagebox.showerror("Signup Failed", f"Database error: {e}")
    except Exception as e:
        messagebox.showerror("Signup Failed", f"Unexpected error: {e}")

# Function to handle login
def login():
    username = entry_username.get()
    password = entry_password.get()

    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    if user:
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        root.after(100, run_main)  # Schedule run_main to be called after 100ms
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Function to run main.py
def run_main():
    root.destroy()  # Close the login window
    subprocess.run(["python", "main.py"])  # Run main.py

# Function to show login frame
def show_login_frame():
    login_frame.pack(pady=20, expand=True)
    signup_frame.pack_forget()
    admin_frame.pack_forget()
    if 'user_details_frame' in globals():
        user_details_frame.pack_forget()  # Hide user details frame

# Function to show signup frame
def show_signup_frame():
    signup_frame.pack(pady=20, expand=True)
    login_frame.pack_forget()
    admin_frame.pack_forget()
    if 'user_details_frame' in globals():
        user_details_frame.pack_forget()  # Hide user details frame

# Function to show admin frame
def show_admin_frame():
    login_frame.pack_forget()
    signup_frame.pack_forget()
    admin_frame.pack(pady=20, expand=True)
    if 'user_details_frame' in globals():
        user_details_frame.pack_forget()  # Hide user details frame

# Function to handle admin login
def admin_login():
    username = entry_admin_username.get()
    password = entry_admin_password.get()

    c.execute("SELECT * FROM admin WHERE username = ? AND password = ?", (username, password))
    if c.fetchone():
        show_user_details_frame()  # Show user details frame
    else:
        messagebox.showerror("Admin Login Failed", "Invalid admin username or password.")

# Function to handle admin registration
def admin_register():
    username = entry_admin_username.get()
    password = entry_admin_password.get()

    if not username or not password:
        messagebox.showerror("Admin Registration Failed", "Username and password cannot be empty.")
        return

    # Check if admin details are already set
    c.execute("SELECT * FROM admin")
    if c.fetchone():
        messagebox.showerror("Admin Registration Failed", "Admin details are already set.")
        return

    try:
        c.execute("INSERT INTO admin (username, password) VALUES (?, ?)", 
                  (username, password))
        conn.commit()
        messagebox.showinfo("Admin Registration Successful", "Admin registered successfully.")
        show_login_frame()
    except sqlite3.Error as e:
        messagebox.showerror("Admin Registration Failed", f"Database error: {e}")
    except Exception as e:
        messagebox.showerror("Admin Registration Failed", f"Unexpected error: {e}")

def fetch_user_details():
    c.execute("SELECT username FROM users")
    users = c.fetchall()
    return users

def refresh_user_list(tree):
    # Clear current entries in the tree
    for item in tree.get_children():
        tree.delete(item)
    
    # Fetch updated user details
    users = fetch_user_details()
    for user in users:
        tree.insert('', tk.END, values=user)

def delete_user(username):
    try:
        c.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        messagebox.showinfo("User Deletion", f"User '{username}' deleted successfully.")
        
        # Refresh the user list in the Treeview
        refresh_user_list(tree)

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database error: {e}")

def show_user_details_frame():
    login_frame.pack_forget()
    signup_frame.pack_forget()
    admin_frame.pack_forget()

    global user_details_frame, tree
    user_details_frame = tk.Frame(root, padx=20, pady=20, bg="#e0f7fa")
    user_details_frame.pack(pady=20, expand=True)

    tk.Label(user_details_frame, text="*User Details*", font=("Arial", 16, "bold"), bg="#e0f7fa").pack(pady=10)

    # Create treeview for displaying user details
    columns = ('*Username*',)
    tree = ttk.Treeview(user_details_frame, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    refresh_user_list(tree)  # Initial population of the Treeview

    tree.pack(expand=True, fill='both')

    # Delete button
    def on_delete():
        selected_item = tree.selection()
        if selected_item:
            username = tree.item(selected_item, 'values')[0]  # Get the username
            delete_user(username)
        else:
            messagebox.showwarning("Delete User", "Please select a user to delete.")

    delete_button = tk.Button(user_details_frame, text="*Delete Selected User*", command=on_delete, font=("Arial", 12, "bold"), bg="green", fg="white")
    delete_button.pack(pady=10)

    # Back to Signup/Login button
    back_to_signup_login_button = tk.Button(user_details_frame, text="*Back to Signup/Login*", command=show_signup_frame, font=("Arial", 12, "bold"), bg="green", fg="white")
    back_to_signup_login_button.pack(pady=10)

# Function to retrieve and show admin credentials
def show_admin_credentials():
    c.execute("SELECT username, password FROM admin")
    admin = c.fetchone()
    if admin:
        messagebox.showinfo("Admin Credentials", f"Admin Username: {admin[0]}\nAdmin Password: {admin[1]}")
    else:
        messagebox.showerror("Error", "No admin found in the database.")

# Create main window
root = tk.Tk()
root.title("*Login and Signup*")
root.geometry("500x400")
root.configure(bg="#b2ebf2")

# Login Frame
login_frame = tk.Frame(root, padx=20, pady=20, bg="#b2ebf2")
login_frame.pack(pady=20, expand=True)

tk.Label(login_frame, text="*Username*", font=("Arial", 12, "bold"), bg="#b2ebf2").grid(row=0, column=0, padx=10, pady=10)
entry_username = tk.Entry(login_frame, font=("Arial", 12, "bold"), width=30)
entry_username.grid(row=0, column=1, padx=10, pady=10)

tk.Label(login_frame, text="*Password*", font=("Arial", 12, "bold"), bg="#b2ebf2").grid(row=1, column=0, padx=10, pady=10)
entry_password = tk.Entry(login_frame, show='*', font=("Arial", 12, "bold"), width=30)
entry_password.grid(row=1, column=1, padx=10, pady=10)

login_button = tk.Button(login_frame, text="*Log In*", command=login, font=("Arial", 12, "bold"), width=15, bg="green", fg="white")
login_button.grid(row=2, columnspan=2, pady=20)

signup_link = tk.Button(login_frame, text="*New user? Sign Up*", command=show_signup_frame, font=("Arial", 12, "bold"), width=15, bg="green", fg="white")
signup_link.grid(row=3, columnspan=2, pady=10)

admin_link = tk.Button(login_frame, text="*Admin Login*", command=show_admin_frame, font=("Arial", 12, "bold"), width=15, bg="green", fg="white")
admin_link.grid(row=4, columnspan=2, pady=10)

# Signup Frame
signup_frame = tk.Frame(root, padx=20, pady=20, bg="#b2ebf2")
signup_frame.pack_forget()

tk.Label(signup_frame, text="*Username*", font=("Arial", 12, "bold"), bg="#b2ebf2").grid(row=0, column=0, padx=10, pady=10)
entry_signup_username = tk.Entry(signup_frame, font=("Arial", 12, "bold"), width=30)
entry_signup_username.grid(row=0, column=1, padx=10, pady=10)

tk.Label(signup_frame, text="*Password*", font=("Arial", 12, "bold"), bg="#b2ebf2").grid(row=1, column=0, padx=10, pady=10)
entry_signup_password = tk.Entry(signup_frame, show='*', font=("Arial", 12, "bold"), width=30)
entry_signup_password.grid(row=1, column=1, padx=10, pady=10)

signup_button = tk.Button(signup_frame, text="*Sign Up*", command=signup, font=("Arial", 12, "bold"), width=15, bg="green", fg="white")
signup_button.grid(row=2, columnspan=2, pady=20)

back_to_login_button = tk.Button(signup_frame, text="*Back to Login*", command=show_login_frame, font=("Arial", 12, "bold"), width=15, bg="green", fg="white")
back_to_login_button.grid(row=3, columnspan=2, pady=10)

# Admin Frame
admin_frame = tk.Frame(root, padx=20, pady=20, bg="#b2ebf2")
admin_frame.pack_forget()

tk.Label(admin_frame, text="*Admin Username*", font=("Arial", 12, "bold"), bg="#b2ebf2").grid(row=0, column=0, padx=10, pady=10)
entry_admin_username = tk.Entry(admin_frame, font=("Arial", 12, "bold"), width=30)
entry_admin_username.grid(row=0, column=1, padx=10, pady=10)

tk.Label(admin_frame, text="*Admin Password*", font=("Arial", 12, "bold"), bg="#b2ebf2").grid(row=1, column=0, padx=10, pady=10)
entry_admin_password = tk.Entry(admin_frame, show='*', font=("Arial", 12, "bold"), width=30)
entry_admin_password.grid(row=1, column=1, padx=10, pady=10)

admin_login_button = tk.Button(admin_frame, text="*Admin Log In*", command=admin_login, font=("Arial", 12, "bold"), width=15, bg="green", fg="white")
admin_login_button.grid(row=2, columnspan=2, pady=10)

# Admin Registration Button
admin_register_button = tk.Button(admin_frame, text="*Register Admin*", command=admin_register, font=("Arial", 12, "bold"), width=15, bg="blue", fg="white")
admin_register_button.grid(row=3, columnspan=2, pady=10)

# Show Admin Credentials Button
show_credentials_button = tk.Button(admin_frame, text="*Show Admin Credentials*", command=show_admin_credentials, font=("Arial", 12, "bold"), width=20, bg="orange", fg="white")
show_credentials_button.grid(row=4, columnspan=2, pady=10)

# Start with the login frame
show_login_frame()

# Run the application
root.mainloop()
