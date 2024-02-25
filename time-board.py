# Copyright (C) 2024 wwhai
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import tkinter as tk
from time import strftime


def update_time():
    current_time = strftime("%Y-%m-%d %H:%M:%S")
    label.config(text=current_time)
    label.after(1000, update_time)  # 每秒更新一次时间


# 创建主窗口
root = tk.Tk()
root.title("Current Time")

# 创建标签来显示时间
label = tk.Label(
    root, font=("calibri", 40, "bold"), background="black", foreground="white"
)
label.pack(padx=20, pady=20)

# 更新时间
update_time()

# 运行主循环
root.mainloop()
