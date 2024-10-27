import tkinter as tk
from client import Client
from tkinter import ttk, messagebox


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Prompt")
        self.root.geometry("400x400")
        self.root.minsize(400, 400)
        self.root.configure(bg="#F0F3F9")

        self.style = ttk.Style()
        self.style.configure("TFrame", background="#F0F3F9")
        self.style.configure("TLabel", background="#F0F3F9", font=("Segoe UI", 12))
        self.style.configure("TButton", font=("Segoe UI", 10), padding=5)
        self.style.map("TButton", background=[("active", "#e0e0e0")])

        self.entry_username = None
        self.entry_password = None
        self.entry_first_name = None
        self.entry_reg_login = None
        self.entry_reg_password = None

        self.login_frame = self.create_login_frame()
        self.registration_frame = self.create_registration_frame()

        self.show_login()

    def create_login_frame(self):
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill='both', expand=True)

        # Add a title label
        title_label = ttk.Label(frame, text="Login", font=("Segoe UI", 18))
        title_label.pack(pady=(0, 20))

        # Username label and entry
        label_username = ttk.Label(frame, text="Username:")
        label_username.pack(pady=5)
        self.entry_username = ttk.Entry(frame, width=40)
        self.entry_username.pack(pady=5)

        # Password label and entry
        label_password = ttk.Label(frame, text="Password:")
        label_password.pack(pady=5)
        self.entry_password = ttk.Entry(frame, show="*", width=40)
        self.entry_password.pack(pady=5)

        # Arrange buttons horizontally using grid
        button_frame = ttk.Frame(frame)  # Create a frame for buttons
        button_frame.pack(pady=(20, 5))

        login_button = ttk.Button(button_frame, text="Login", command=self.login)
        login_button.grid(row=0, column=0, padx=(0, 10))  # Add padding between buttons

        register_button = ttk.Button(button_frame, text="Register", command=self.show_registration)
        register_button.grid(row=0, column=1)

        return frame

    def create_registration_frame(self):
        frame = ttk.Frame(self.root, padding="20")

        # Registration title label
        register_title_label = ttk.Label(frame, text="Register", font=("Segoe UI", 18))
        register_title_label.pack(pady=(0, 20))

        # First name label and entry
        label_first_name = ttk.Label(frame, text="First Name:")
        label_first_name.pack(pady=5)
        self.entry_first_name = ttk.Entry(frame, width=40)
        self.entry_first_name.pack(pady=5)

        # Username label and entry
        label_reg_login = ttk.Label(frame, text="Username:")
        label_reg_login.pack(pady=5)
        self.entry_reg_login = ttk.Entry(frame, width=40)
        self.entry_reg_login.pack(pady=5)

        # Password label and entry
        label_reg_password = ttk.Label(frame, text="Password:")
        label_reg_password.pack(pady=5)
        self.entry_reg_password = ttk.Entry(frame, show="*", width=40)
        self.entry_reg_password.pack(pady=5)

        # Arrange buttons for registration horizontally using grid
        register_button_frame = ttk.Frame(frame)  # Create a frame for buttons
        register_button_frame.pack(pady=(20, 5))

        register_submit_button = ttk.Button(register_button_frame, text="Register", command=self.register)
        register_submit_button.grid(row=0, column=0, padx=(0, 10))  # Add padding between buttons

        cancel_button = ttk.Button(register_button_frame, text="Cancel", command=self.cancel_registration)
        cancel_button.grid(row=0, column=1)

        return frame

    def show_login(self):
        self.registration_frame.pack_forget()
        self.login_frame.pack(fill='both', expand=False)

    def show_registration(self):
        self.login_frame.pack_forget()
        self.registration_frame.pack(fill='both', expand=False)

    def cancel_registration(self):
        self.entry_first_name.delete(0, tk.END)
        self.entry_reg_login.delete(0, tk.END)
        self.entry_reg_password.delete(0, tk.END)
        self.show_login()

    def login(self):
        try:
            response = Client.login(self.entry_username.get().lower(), self.entry_password.get())
            messagebox.showinfo("Login Successful", response)
        except Exception as e:
            messagebox.showerror("Login Failed", str(e))

    def register(self):
        try:
            response = Client.register(self.entry_first_name.get(), self.entry_reg_login.get().lower(), self.entry_reg_password.get())
            messagebox.showinfo("Registration Successful", response)
            self.show_registration()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")