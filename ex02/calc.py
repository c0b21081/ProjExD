from ast import Num
import tkinter as tk
import tkinter.messagebox as tkm

def click_number(event):
    btn = event.widget
    num = int(btn["text"])
    tkm.showinfo(f"{num}", f"{num}のボタンが押されました")

root = tk.Tk()
root.title("電卓")
root.geometry("300x500")

r = 0
c = 0

for i in  range(9, -1, -1):
    button = tk.Button(root, text = i, font = ("Times New Roman", 30), width = 4, height = 2)
    button.grid(row = r, column = c)
    c += 1
    if c == 3:
        c = 0
        r += 1

root.mainloop()