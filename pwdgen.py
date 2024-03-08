import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip


def generate_password():
    password = "".join(random.choices(string.ascii_letters + string.digits, k=16))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)


def copy_password():
    password = password_entry.get()
    pyperclip.copy(password)
    messagebox.showinfo("Password Generator", "Password copied to clipboard!")


from datetime import datetime


def save_to_file():
    password = password_entry.get()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("password.txt", "a") as file:
        file.write(f"{current_time}: {password}\n")
    messagebox.showinfo("Password Generator", "Password saved to password.txt!")


root = tk.Tk()
root.title("Password Generator")

# 设置窗口不可最大化
root.resizable(False, False)

# 计算窗口在屏幕中的位置
window_width = 400
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# 设置窗口位置
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

password_label = tk.Label(frame, text="Password:")
password_label.grid(row=0, column=0, padx=5, pady=5)

password_entry = tk.Entry(frame, width=30)
password_entry.grid(row=0, column=1, padx=5, pady=5)

generate_button = tk.Button(frame, text="Generate", command=generate_password)
generate_button.grid(row=1, column=0, padx=5, pady=5)

copy_button = tk.Button(frame, text="Copy", command=copy_password)
copy_button.grid(row=1, column=1, padx=5, pady=5)

save_button = tk.Button(frame, text="Save to File", command=save_to_file)
save_button.grid(row=1, column=2, padx=5, pady=5)

# 默认填充一个随机密码
generate_password()

root.mainloop()
