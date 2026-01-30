#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox

# IMPORT CORE LOGIC
from analyzer import analyze
from utils  import generate_password


# ---------------- GUI LOGIC ----------------

def check_password():
    password = entry.get()

    if not password:
        messagebox.showwarning("PascoLock", "Please enter a password")
        return

    result = analyze(password)

    output.config(
        text=(
            f"Score       : {result['score']}/100\n"
            f"Entropy     : {result['entropy']} bits\n"
            f"Crack Time  : {result['crack_time']}\n"
            f"Breach Hits : {result['breach']}"
        )
    )


def generate_pwd():
    pwd = generate_password()
    entry.delete(0, tk.END)
    entry.insert(0, pwd)
    check_password()


# ---------------- GUI WINDOW ----------------

root = tk.Tk()
root.title("PascoLock – Password Security Tool")
root.geometry("420x320")
root.resizable(False, False)

# ---------------- UI ELEMENTS ----------------

title = tk.Label(
    root,
    text="PascoLock",
    font=("Arial", 18, "bold")
)
title.pack(pady=10)

subtitle = tk.Label(
    root,
    text="Advanced Password Checker (Kali Linux)",
    font=("Arial", 10)
)
subtitle.pack()

tk.Label(root, text="Enter Password:", font=("Arial", 10)).pack(pady=10)

entry = tk.Entry(root, width=35, show="*")
entry.pack()

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(
    btn_frame,
    text="Check Password",
    command=check_password,
    width=15
).grid(row=0, column=0, padx=5)

tk.Button(
    btn_frame,
    text="Generate Strong",
    command=generate_pwd,
    width=15
).grid(row=0, column=1, padx=5)

output = tk.Label(
    root,
    text="",
    font=("Courier", 10),
    justify="left"
)
output.pack(pady=15)

# ---------------- START GUI ----------------
root.mainloop()
