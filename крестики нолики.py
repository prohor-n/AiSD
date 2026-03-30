import tkinter as tk
from tkinter import messagebox

b = [['']*3 for _ in range(3)]
btn = [[None]*3 for _ in range(3)]
over = [False]

def reset():
    global b
    b = [['']*3 for _ in range(3)]
    over[0] = False
    for r in range(3):
        for c in range(3):
            btn[r][c].config(text='', state='normal')

def put(r,c,s):
    b[r][c] = s
    color = "red" if s == "X" else "blue"
    btn[r][c].config(text=s, state='disabled', disabledforeground=color)

def check(s):
    for i in range(3):
        if b[i][0]==b[i][1]==b[i][2]==s: return True
        if b[0][i]==b[1][i]==b[2][i]==s: return True
    if b[0][0]==b[1][1]==b[2][2]==s or b[0][2]==b[1][1]==b[2][0]==s: return True
    return False

def full():
    return all(b[r][c] for r in range(3) for c in range(3))

def announce(winner):
    over[0] = True
    if winner == 'Draw':
        messagebox.showinfo("Результат", "Ничья")
    else:
        messagebox.showinfo("Результат", f"Победил {winner}")

def player(r,c):
    if b[r][c] or over[0]: return
    put(r,c,'X')
    if check('X'):
        announce('X'); return
    if full():
        announce('Draw'); return
    bot()  

def bot():
    if over[0]: return
    rc = best()
    if rc:
        put(rc[0], rc[1], 'O')
    if check('O'):
        announce('O'); return
    if full():
        announce('Draw'); return

def best():
    def try_move(sym):
        for r in range(3):
            for c in range(3):
                if not b[r][c]:
                    b[r][c] = sym
                    ok = check(sym)
                    b[r][c] = ''
                    if ok: return (r,c)
        return None
    x = try_move('O')   # попытка выиграть
    if x: return x
    x = try_move('X')   # блокировка игрока
    if x: return x
    if not b[1][1]: return (1,1)  # центр 
    pairs = [((0,0),(2,2)),((0,2),(2,0)),((2,2),(0,0)),((2,0),(0,2))]
    for a,bp in pairs:
        if b[a[0]][a[1]]=='X' and b[bp[0]][bp[1]]=='':
            return bp
    for r,c in [(0,0),(0,2),(2,0),(2,2),(0,1),(1,0),(1,2),(2,1)]:
        if not b[r][c]: return (r,c)
    return None
# гуишка 
root = tk.Tk()
root.title("Крестики-нолики")
tk.Button(root, text="Новая игра", command=reset).grid(row=0, column=0, columnspan=3, sticky="we")
for r in range(3):
    for c in range(3):
        btn[r][c] = tk.Button(root, text='', font=('Arial',48),
                              width=3, height=1,
                              command=lambda r=r,c=c: player(r,c))
        btn[r][c].grid(row=r+1, column=c)
root.update_idletasks()
x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
root.geometry(f"+{x}+{y}")
root.mainloop()
