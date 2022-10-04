import tkinter as tk
import tkinter.messagebox as tkm

#左クリック
def button_click(event):
    btn = event.widget
    num = btn["text"]
    entry.insert(tk.END, num)

#イコール
def click_equal(event):
    eqn = entry.get()
    #電話番号を打ち込むと反応する
    if eqn == "042-637-2111":
        tkm.askyesno("call", f"{eqn}は東京工科大学の電話番号です。お掛けになりますか？")   #追加機能
    res = eval(eqn)
    entry.delete(0, tk.END)
    entry.insert(tk.END, res)
    
root = tk.Tk()
root.title("電卓")
root.geometry("400x690")

entry = tk.Entry(root, width = 10, font = (", 38"), bg = "blue", justify = "right")
entry.grid(row = 0, column = 0, columnspan = 3)

#ボタン
r = 1
c = 0
number = list(range(9, -1, -1))
plus = ["/", "*", "-", "+"]

#数字
for i in number:
    button = tk.Button(root, text = i, font = ("Times New Roman", 30), width = 4, height = 2, bg = "blue", fg = "white")  
    button.bind("<1>", button_click)
    button.grid(row = r, column = c)
    c += 1
    if c == 3:
        c = 0
        r += 1

#イコール
button = tk.Button(root, text = "=", font = ("Times New Roman", 30), width = 4, height = 2, bg = "blue", fg = "white")  
button.bind("<1>", click_equal)
button.grid(row = r, column = c)

r = 1   #リセット
#四則演算
for j in plus:
    button = tk.Button(root, text = j, font = ("Times New Roman", 30), width = 4, height = 2, bg = "blue", fg = "white")  
    button.bind("<1>", button_click)
    button.grid(row = r, column = 4)
    r += 1

root.mainloop()