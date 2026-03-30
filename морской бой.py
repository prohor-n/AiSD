import tkinter as tk
from tkinter import messagebox
import random

class Ship:
    def __init__(self, cells):
        self.cells = set(cells)
        self.hits = set()
    def is_sunk(self): return self.hits == self.cells

class Board:
    def __init__(self):
        self.grid = [[0]*10 for _ in range(10)]
        self.ships, self.shots = [], set()

    def can_place(self, r, c, size, horiz):
        cells = [(r, c+i) if horiz else (r+i, c) for i in range(size)]
        for rr, cc in cells:
            if not (0<=rr<10 and 0<=cc<10) or self.grid[rr][cc] != 0: return False
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    nr, nc = rr+dr, cc+dc
                    if 0<=nr<10 and 0<=nc<10 and self.grid[nr][nc] == 1: return False
        return True

    def place_ship(self, r, c, size, horiz):
        if not self.can_place(r, c, size, horiz): return False
        cells = [(r, c+i) if horiz else (r+i, c) for i in range(size)]
        self.ships.append(Ship(cells))
        for rr, cc in cells: self.grid[rr][cc] = 1
        return True

    def shoot(self, r, c):
        if (r, c) in self.shots: return None
        self.shots.add((r, c))
        if self.grid[r][c] == 1:
            self.grid[r][c] = 2
            for s in self.ships:
                if (r, c) in s.cells:
                    s.hits.add((r, c))
                    res = 'sunk' if s.is_sunk() else 'hit'
                    if res == 'sunk': self.mark_around(s)
                    return res
        self.grid[r][c] = 3
        return 'miss'

    def mark_around(self, ship):
        for rr, cc in ship.cells:
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    nr, nc = rr+dr, cc+dc
                    if 0<=nr<10 and 0<=nc<10 and self.grid[nr][nc] == 0:
                        self.grid[nr][nc] = 3; self.shots.add((nr, nc))
            self.grid[rr][cc] = 4

class SeaBattle:
    def __init__(self, root):
        self.root = root
        self.root.title("Морской Бой: Исправленный AI")
        self.cell, self.idx, self.horiz = 35, 0, True
        self.sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self.colors = {0: "#006994", 1: "#444444", 2: "orange", 3: "#d3d3d3", 4: "red"}
        self.setup_ui()
        self.reset_game()

    def setup_ui(self):
        f = tk.Frame(self.root); f.pack(pady=10)
        tk.Button(f, text="Поворот", command=self.rot, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(f, text="Случайно", command=self.random_place, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(f, text="Заново", command=self.reset_game, width=10).pack(side=tk.LEFT, padx=5)
        self.lbl = tk.Label(self.root, text="", font=("Arial", 12, "bold"))
        self.lbl.pack()
        bf = tk.Frame(self.root); bf.pack(pady=10, padx=10)
        self.cp = tk.Canvas(bf, width=350, height=350, bg="#006994")
        self.cc = tk.Canvas(bf, width=350, height=350, bg="#006994")
        self.cp.pack(side=tk.LEFT, padx=10); self.cc.pack(side=tk.LEFT, padx=10)
        self.cp.bind("<Button-1>", self.p_click); self.cp.bind("<Motion>", self.p_hover)
        self.cc.bind("<Button-1>", self.c_click)

    def reset_game(self):
        self.pb, self.cb = Board(), Board()
        self.phase, self.idx, self.lock = "setup", 0, False
        self.targets = [(r, c) for r in range(10) for c in range(10)]
        random.shuffle(self.targets); self.stack = []
        self.lbl.config(text=f"Ставим {self.sizes[0]}-палубный")
        self.draw()

    def rot(self): self.horiz = not self.horiz

    def random_place(self):
        self.pb = Board()
        for s in self.sizes:
            while not self.pb.place_ship(random.randint(0,9), random.randint(0,9), s, random.choice([True,False])): pass
        self.start_battle()

    def p_hover(self, e):
        if self.phase != "setup": return
        self.draw(); r, c = e.y // self.cell, e.x // self.cell
        size = self.sizes[self.idx]
        color = "#888888" if self.pb.can_place(r, c, size, self.horiz) else "#ff6666"
        for i in range(size):
            rr, cc = (r, c+i) if self.horiz else (r+i, c)
            if 0<=rr<10 and 0<=cc<10:
                self.cp.create_rectangle(cc*self.cell, rr*self.cell, (cc+1)*self.cell, (rr+1)*self.cell, fill=color, stipple="gray50")

    def p_click(self, e):
        if self.phase != "setup": return
        r, c = e.y // self.cell, e.x // self.cell
        if self.pb.place_ship(r, c, self.sizes[self.idx], self.horiz):
            self.idx += 1
            if self.idx >= len(self.sizes): self.start_battle()
            else: self.lbl.config(text=f"Ставим {self.sizes[self.idx]}-палубный")
            self.draw()

    def start_battle(self):
        self.phase = "play"; self.lbl.config(text="Твой ход!"); self.lock = False
        for s in self.sizes:
            while not self.cb.place_ship(random.randint(0,9), random.randint(0,9), s, random.choice([True,False])): pass
        self.draw()

    def draw_cell(self, cv, r, c, v, is_p):
        x, y = c*self.cell, r*self.cell
        color = self.colors[v] if (is_p or v > 1) else self.colors[0]
        cv.create_rectangle(x, y, x+self.cell, y+self.cell, fill=color, outline="#004d6b")
        if v == 2: cv.create_oval(x+8, y+8, x+27, y+27, fill="orange", outline="")
        elif v == 3:
            cv.create_rectangle(x, y, x+self.cell, y+self.cell, fill="#d3d3d3", outline="#004d6b")
            cv.create_line(x+12, y+12, x+23, y+23, fill="#666"); cv.create_line(x+23, y+12, x+12, y+23, fill="#666")
        elif v == 4:
            cv.create_line(x+5, y+5, x+30, y+30, fill="red", width=3); cv.create_line(x+30, y+5, x+5, y+30, fill="red", width=3)

    def draw(self):
        self.cp.delete("all"); self.cc.delete("all")
        for r in range(10):
            for c in range(10):
                self.draw_cell(self.cp, r, c, self.pb.grid[r][c], True)
                self.draw_cell(self.cc, r, c, self.cb.grid[r][c], False)

    def c_click(self, e):
        if self.phase != "play" or self.lock: return
        r, c = e.y // self.cell, e.x // self.cell
        res = self.cb.shoot(r, c)
        if res:
            self.draw(); self.check()
            if res == "miss": 
                self.lock = True
                self.lbl.config(text="Ход компьютера...")
                self.root.after(600, self.bot_turn)

    def bot_turn(self):
        if self.phase != "play": return
        if self.stack:
            r, c = self.stack.pop(0)
        else:
            r, c = self.targets.pop()
        
        while (r, c) in self.pb.shots and self.targets:
            if self.stack: r, c = self.stack.pop(0)
            else: r, c = self.targets.pop()

        res = self.pb.shoot(r, c)
        if res:
            self.draw(); self.check()
            if res in ("hit", "sunk"):
                if res == "hit":
                    for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                        nr, nc = r+dr, c+dc
                        if 0<=nr<10 and 0<=nc<10 and (nr, nc) not in self.pb.shots:
                            if (nr, nc) not in self.stack: self.stack.append((nr, nc))
                else: self.stack = []
                self.root.after(600, self.bot_turn)
            else:
                self.lock = False
                self.lbl.config(text="Твой ход!")

    def check(self):
        if all(s.is_sunk() for s in self.cb.ships): messagebox.showinfo("!", "Победа!"); self.reset_game()
        elif all(s.is_sunk() for s in self.pb.ships): messagebox.showinfo("!", "Бот победил!"); self.reset_game()

if __name__ == "__main__":
    root = tk.Tk(); SeaBattle(root); root.mainloop()