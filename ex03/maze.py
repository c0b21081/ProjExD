import tkinter as tk
#練習8
import maze_maker as mm

from random import randint
import tkinter.messagebox as tkm

#練習5
def key_down(event):
    global key
    key = event.keysym

#練習6
def key_up(event):
    global key
    key = ""

#練習7
def main_proc():
    global mx, my
    global cx, cy
    global tori
    global tmr
    tmr = tmr+1

    #3:ゴールしたときの称賛
    if mx == 13 and my == 7:                        #4:ゴールまでにかかった時間
        tkm.showinfo("Goal!", f"もう一回遊べるドン！！{tmr/10}秒かかりました")
        mx, my = 1, 1
        cx, cy = mx*100+50, my*100+50
    if key == "Up":
        my -= 1
    if key == "Down":
        my += 1
    if key == "Left":
        mx -= 1
    if key == "Right":
        mx += 1
    if maze_lst[my][mx] == 0:
        cx, cy = mx*100+50, my*100+50

        #1:パリピこうかとんの実装
        n = randint(0,9)
        tori = tk.PhotoImage(file=f"fig/{n}.png")
        canv.create_image(cx, cy, image=tori, tag="tori")

    else: #壁なら
        if key == "Up":
            my += 1
        if key == "Down":
            my -= 1
        if key == "Left":
            mx += 1
        if key == "Right":
            mx -= 1
    canv.coords("tori", cx, cy)
    root.after(100, main_proc)

#練習9
maze_lst = mm.make_maze(15, 9)
print(maze_lst)   #1:壁 0:床

if __name__ == "__main__":

    root = tk.Tk()
    tmr = 0

    #練習１
    root.title("迷えるこうかとん")
    
    #練習2
    canv = tk.Canvas(root, width=1500, height=900, bg="black")
    canv.pack()

    #練習9,10
    maze_lst = mm.make_maze(15, 9)
    mm.show_maze(canv, maze_lst)

    #2:StartとGoalの表示
    start = tk.PhotoImage(file="fig/10.png")
    goal = tk.PhotoImage(file="fig/11.png")
    x, y = 1350, 750
    canv.create_image(x-1200, y-600, image=start, tag="start")
    canv.create_image(x, y, image=goal, tag="goal")
    
    #練習3
    tori = tk.PhotoImage(file="fig/5.png")
    mx, my = 1, 1
    cx, cy = mx*100+50, my*100+50
    canv.create_image(cx, cy, image=tori, tag="tori")

    #練習4
    key = "" # 現在押されているキーを表す

    #練習5, 6
    root.bind("<KeyPress>", key_down)
    root.bind("<KeyRelease>", key_up)
    
    #練習7
    main_proc()

    root.mainloop()