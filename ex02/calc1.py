print("hello world")

import tkinter as tk   #モジュールに別名を付ける
import tkinter.messagebox as tkm

def button_click(event):
    btn = event.widget
    txt = btn["text"]
    tkm.showwarning("警告", f"{txt}ボタンが押されました")
root = tk.Tk()   #tkモジュールの中のTkインスタンスを生成
root.title("おためしか")
root.geometry("500x200")

label = tk.Label(root,
                text = "ラベルを書いてみた件",
                font = ("Ricty Diminished", 20)
                )   #(親ウィンドウ、文字列、(フォント、フォントサイズ))
label.pack()

button = tk.Button(root, text = "押すな", font = ("", 30), bg = "white")
button.bind("<1>", button_click)
button.pack()

entry = tk.Entry(root, width = 30)
entry.insert(tk.END, "kazuto")
entry.pack()

root.mainloop()   #ウィンドウを表示する


