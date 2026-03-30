# сегментация поворот квадратов 

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import math
import random
import json

class Square:
    def __init__(self, x, y, size, color="", angle=0):
        self.x, self.y, self.size, self.color, self.angle = float(x), float(y), float(size), color, angle

    def symmetric_segmentation(self, segments):
        segment_size = self.size / segments
        return [Square(self.x - self.size/2 + segment_size/2 + j * segment_size,
                       self.y - self.size/2 + segment_size/2 + i * segment_size,
                       segment_size, self.color)
                for i in range(segments) for j in range(segments)]

    def rotate(self, angle):
        self.angle = (self.angle + angle) % 360
        return self

    def change_color(self, color):
        self.color = color
        return self

    def get_vertices(self):
        half = self.size / 2
        rad = math.radians(self.angle)
        corners = [(self.x - half, self.y - half), (self.x + half, self.y - half),
                   (self.x + half, self.y + half), (self.x - half, self.y + half)]
        return [(math.cos(rad)*(x - self.x) - math.sin(rad)*(y - self.y) + self.x,
                 math.sin(rad)*(x - self.x) + math.cos(rad)*(y - self.y) + self.y) for x,y in corners]

class SquareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("создание квадратов")
        self.root.geometry("820x600")
        self.squares = []
        self.current = None
        self.selected_color = "red"
        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left = ttk.Frame(frame)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10))
        right = ttk.Frame(frame)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(right, bg="white", width=500, height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.select_square)

        self.x_entry = self.create_labeled_entry(left, "X:", "250")
        self.y_entry = self.create_labeled_entry(left, "Y:", "250")
        self.size_entry = self.create_labeled_entry(left, "Размер:", "100")

        self.color_btn = ttk.Button(left, text="Выбрать цвет", command=self.choose_color)
        self.color_btn.pack(fill=tk.X)

        self.add_btn = ttk.Button(left, text="Создать квадрат", command=self.create_square)
        self.add_btn.pack(fill=tk.X, pady=5)

        self.segments_entry = self.create_labeled_entry(left, "Сегментов:", "2")
        ttk.Button(left, text="Выполнить сегментацию", command=self.perform_segmentation).pack(fill=tk.X, pady=5)

        self.angle_entry = self.create_labeled_entry(left, "Угол поворота:", "45")
        ttk.Button(left, text="Повернуть", command=self.rotate_square).pack(fill=tk.X, pady=5)

        ttk.Button(left, text="Случайный цвет", command=self.random_color).pack(fill=tk.X, pady=5)
        ttk.Button(left, text="Загрузить из файла", command=self.load_from_file).pack(fill=tk.X, pady=5)
        ttk.Button(left, text="Сохранить в файл", command=self.save_to_file).pack(fill=tk.X, pady=5)
        ttk.Button(left, text="Очистить холст", command=self.clear_canvas).pack(fill=tk.X, pady=20)

    def create_labeled_entry(self, parent, label, default):
        ttk.Label(parent, text=label).pack()
        entry = ttk.Entry(parent)
        entry.pack()
        entry.insert(0, default)
        return entry

    def choose_color(self):
        color = colorchooser.askcolor(title="Выберите цвет")
        if color[1]:
            self.selected_color = color[1]

    def create_square(self):
        try:
            x, y = float(self.x_entry.get()), float(self.y_entry.get())
            size = float(self.size_entry.get())
            if size <= 0:
                messagebox.showerror("Ошибка", "Размер должен быть положительным")
                return
            sq = Square(x, y, size, self.selected_color)
            self.squares.append(sq)
            self.current = sq
            self.visualize()
        except Exception:
            messagebox.showerror("Ошибка", "Некорректные данные")

    def perform_segmentation(self):
        if not self.current:
            messagebox.showwarning("Внимание", "Выберите квадрат")
            return
        try:
            n = int(self.segments_entry.get())
            if n <= 0:
                messagebox.showerror("Ошибка", "Неверное количество сегментов")
                return
            self.squares.remove(self.current)
            self.squares.extend(self.current.symmetric_segmentation(n))
            self.current = None
            self.visualize()
        except Exception:
            messagebox.showerror("Ошибка", "Некорректные данные")

    def rotate_square(self):
        if not self.current:
            messagebox.showwarning("Внимание", "Выберите квадрат")
            return
        try:
            angle = float(self.angle_entry.get())
            self.current.rotate(angle)
            self.visualize()
        except Exception:
            messagebox.showerror("Ошибка", "Некорректные данные")

    def random_color(self):
        if not self.current:
            messagebox.showwarning("Внимание", "Выберите квадрат")
            return
        self.current.change_color(random.choice(["black", "red", "blue", "green", "yellow", "purple", "orange"]))
        self.visualize()

    def load_from_file(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if path:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.squares = [Square(**sq) for sq in data]
            self.current = None
            self.visualize()

    def save_to_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if path:
            data = [{"x": sq.x, "y": sq.y, "size": sq.size, "color": sq.color, "angle": sq.angle} for sq in self.squares]
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    def clear_canvas(self):
        self.squares.clear()
        self.current = None
        self.visualize()

    def select_square(self, event):
        x, y = event.x, event.y
        for sq in reversed(self.squares):
            verts = sq.get_vertices()
            xs, ys = zip(*verts)
            if min(xs) <= x <= max(xs) and min(ys) <= y <= max(ys):
                self.current = sq
                self.visualize()
                break

    def draw_grid(self):
        step = 50
        w = 10000
        h = 10000
        line_color = "#cccccc"
        font = ("Arial", 8)
        for x in range(0, w, step):
            self.canvas.create_line(x, 0, x, h, fill=line_color)
            self.canvas.create_text(x+2, 10, text=str(x), fill=line_color, anchor="nw", font=font)
        for y in range(0, h, step):
            self.canvas.create_line(0, y, w, y, fill=line_color)
            if y > 0:
                self.canvas.create_text(2, y+2, text=str(y), fill=line_color, anchor="nw", font=font)

    def visualize(self):
        self.canvas.delete("all")
        self.draw_grid()
        for sq in self.squares:
            verts = sq.get_vertices()
            points = [coord for v in verts for coord in v]
            self.canvas.create_polygon(points, fill=sq.color, outline="black", width=2)
            if sq == self.current:
                self.canvas.create_oval(sq.x - 5, sq.y - 5, sq.x + 5, sq.y + 5, fill="red", outline="")
    
if __name__ == "__main__":
    root = tk.Tk()
    app = SquareApp(root)
    root.mainloop()
