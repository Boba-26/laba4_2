import tkinter as tk
from tkinter import messagebox, font as tkfont
import ctypes
import os

# --- Вспомогательная функция для центрирования окон ---
def center_popup(win, parent):
    win.update_idletasks()
    w, h = win.winfo_width(), win.winfo_height()
    pw, ph = parent.winfo_width(), parent.winfo_height()
    px, py = parent.winfo_x(), parent.winfo_y()
    x = px + (pw // 2) - (w // 2)
    y = py + (ph // 2) - (h // 2)
    win.geometry(f"+{x}+{y}")

# --- Диалоговые окна ---

class SingleValueDialog(tk.Toplevel):
    def __init__(self, parent, title="Ввод", label_text="Значение:"):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.result = None
        f = tk.Frame(self, padx=20, pady=10); f.pack()
        tk.Label(f, text=label_text).pack()
        self.entry = tk.Entry(f); self.entry.pack(pady=5); self.entry.focus_set()
        tk.Button(f, text="ОК (Enter)", command=self.confirm).pack(pady=5)
        self.transient(parent); self.grab_set()
        center_popup(self, parent)
        self.bind("<Return>", lambda e: self.confirm())

    def confirm(self):
        try:
            self.result = int(self.entry.get()); self.destroy()
        except ValueError: messagebox.showerror("Ошибка", "Введите целое число!", parent=self)

class InsertDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Вставка элемента")
        self.resizable(False, False); self.result = None
        f = tk.Frame(self, padx=20, pady=10); f.pack()
        tk.Label(f, text="Значение:").pack()
        self.e_val = tk.Entry(f); self.e_val.pack(pady=2); self.e_val.focus_set()
        tk.Label(f, text="Индекс:").pack()
        self.e_idx = tk.Entry(f); self.e_idx.pack(pady=2)
        tk.Button(f, text="ОК (Enter)", command=self.confirm).pack(pady=10)
        self.transient(parent); self.grab_set()
        center_popup(self, parent)
        self.bind("<Return>", lambda e: self.handle_enter())

    def handle_enter(self):
        if self.focus_get() == self.e_val: self.e_idx.focus_set()
        else: self.confirm()

    def confirm(self):
        try:
            self.result = (int(self.e_val.get()), int(self.e_idx.get())); self.destroy()
        except ValueError: messagebox.showerror("Ошибка", "Введите числа!", parent=self)

class RandomDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Случайное заполнение")
        self.resizable(False, False); self.result = None
        f = tk.Frame(self, padx=20, pady=10); f.pack()
        tk.Label(f, text="Кол-во:").pack()
        self.e_n = tk.Entry(f); self.e_n.insert(0, "3"); self.e_n.pack(); self.e_n.focus_set()
        tk.Label(f, text="Мин:").pack()
        self.e_mi = tk.Entry(f); self.e_mi.insert(0, "1"); self.e_mi.pack()
        tk.Label(f, text="Макс:").pack()
        self.e_ma = tk.Entry(f); self.e_ma.insert(0, "100"); self.e_ma.pack()
        tk.Button(f, text="ОК (Enter)", command=self.confirm).pack(pady=10)
        self.transient(parent); self.grab_set()
        center_popup(self, parent)
        self.bind("<Return>", lambda e: self.handle_enter())

    def handle_enter(self):
        curr = self.focus_get()
        if curr == self.e_n: self.e_mi.focus_set()
        elif curr == self.e_mi: self.e_ma.focus_set()
        else: self.confirm()

    def confirm(self):
        try:
            self.result = (int(self.e_n.get()), int(self.e_mi.get()), int(self.e_ma.get())); self.destroy()
        except ValueError: messagebox.showerror("Ошибка", "Введите числа!", parent=self)

# --- Главное приложение ---

class CyclicListGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Лабораторная 4.2: Мультиструктурный список (Python/C++)")
        self.geometry("1300x900")
        self.withdraw()
        
        self.structures = []
        self.current_idx = 0
        self.logic_module = None
        self.use_cpp = False
        self.dialog_active = False
        self.nodes_coords = []
        
        self.init_startup()

    def init_startup(self):
        sw = tk.Toplevel(self); sw.title("Настройка"); sw.geometry("300x160")
        self.mod_choice = tk.StringVar(value="py")
        tk.Radiobutton(sw, text="Python Модуль (.py)", variable=self.mod_choice, value="py").pack(pady=5)
        tk.Radiobutton(sw, text="C++ Модуль (.dll)", variable=self.mod_choice, value="cpp").pack()
        tk.Button(sw, text="Запустить", command=lambda: self.load_module(sw), bg="#4CAF50", fg="white", width=15).pack(pady=15)
        center_popup(sw, self)

    def load_module(self, win):
        if self.mod_choice.get() == "cpp":
            try:
                dll_path = os.path.join(os.path.dirname(__file__), "list_logic.dll")
                self.logic_module = ctypes.CDLL(dll_path)
                
                # --- ВАЖНО: Настройка типов данных для 64-битных систем ---
                # Все функции, принимающие или возвращающие указатель на список, 
                # должны знать, что это c_void_p
                
                # Возвращает адрес новой структуры
                self.logic_module.create_list.restype = ctypes.c_void_p
                
                # Указываем, что первым аргументом всегда идет адрес (указатель)
                self.logic_module.get_count.argtypes = [ctypes.c_void_p]
                self.logic_module.clear_list.argtypes = [ctypes.c_void_p]
                self.logic_module.delete_list_obj.argtypes = [ctypes.c_void_p]
                
                self.logic_module.read_at.argtypes = [ctypes.c_void_p, ctypes.c_int]
                self.logic_module.delete_at.argtypes = [ctypes.c_void_p, ctypes.c_int]
                self.logic_module.insert_at.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
                self.logic_module.fill_random.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]
                
                self.use_cpp = True
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить DLL!\n{e}"); return
        else:
            # Логика для Python модуля остается прежней
            try: 
                import linked_list_py
                self.logic_module = linked_list_py
            except: messagebox.showerror("Ошибка", "linked_list_py.py не найден!"); return
        
        win.destroy(); self.deiconify(); self.build_ui(); self.add_new_struct()

    def build_ui(self):
        top = tk.Frame(self, pady=10, bg="#f5f5f5"); top.pack(side=tk.TOP, fill=tk.X)
        tk.Button(top, text="+ Структура", command=self.add_new_struct, bg="#4CAF50", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="- Структура", command=self.remove_current_struct, bg="#f44336", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        
        btn_f = tk.Frame(top, bg="#f5f5f5"); btn_f.pack(side=tk.RIGHT, padx=20)
        self.cmds = [self.cmd_clear, self.cmd_add_end, self.cmd_insert, self.cmd_read, self.cmd_delete, self.cmd_random]
        lbls = ["1.Очистить", "2.В конец", "3.Вставить", "4.Читать", "5.Удалить", "6.Рандом"]
        for i, t in enumerate(lbls):
            tk.Button(btn_f, text=t, command=self.cmds[i], width=11).grid(row=0, column=i, padx=2)

        container = tk.Frame(self); container.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        self.vs = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.hs = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vs.set, xscrollcommand=self.hs.set)
        self.vs.pack(side=tk.RIGHT, fill=tk.Y); self.hs.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.bind_all("<KeyPress>", self.handle_hotkeys)
        self.bind_all("<Up>", lambda e: self.change_selection(-1))
        self.bind_all("<Down>", lambda e: self.change_selection(1))
        self.bind_all("=", self.handle_plus)
        self.bind_all("+", self.handle_plus)
        self.bind_all("<KP_Add>", self.handle_plus)
        self.bind_all("-", self.handle_minus)
        self.bind_all("<KP_Subtract>", self.handle_minus)

    def handle_plus(self, e): 
        if not self.dialog_active: self.add_new_struct()
    def handle_minus(self, e): 
        if not self.dialog_active: self.remove_current_struct()

    def handle_hotkeys(self, event):
        if self.dialog_active: return 
        if event.char.isdigit():
            idx = int(event.char) - 1
            if 0 <= idx < len(self.cmds): self.cmds[idx]()

    def change_selection(self, delta):
        if self.dialog_active: return
        new_idx = self.current_idx + delta
        if 0 <= new_idx < len(self.structures):
            self.current_idx = new_idx; self.render(); self.scroll_to_current()

    def scroll_to_current(self):
        self.update_idletasks()
        bbox = self.canvas.bbox("all")
        if bbox:
            target_y = (self.current_idx * 280) / float(bbox[3])
            self.canvas.yview_moveto(max(0, target_y - 0.05))

    def render(self):
        self.canvas.delete("all")
        self.nodes_coords = []
        curr_y = 130 
        max_x = 1000
        gap = 50
        node_font = tkfont.Font(family="Arial", size=10, weight="bold")

        for s_idx, struct in enumerate(self.structures):
            active = (s_idx == self.current_idx)
            if active:
                self.canvas.create_rectangle(0, curr_y-110, 5000, curr_y-105, fill="#4CAF50", outline="")
                self.canvas.create_rectangle(0, curr_y+110, 5000, curr_y+115, fill="#4CAF50", outline="")

            color = "#4CAF50" if active else "#ccc"
            self.canvas.create_rectangle(10, curr_y-25, 75, curr_y+45, outline=color, width=2)
            self.canvas.create_text(42, curr_y+10, text=f"СТР {s_idx+1}", font=("Arial", 10, "bold"))

            # Получаем количество элементов
            count = self.logic_module.get_count(struct) if self.use_cpp else struct.count
            
            x_cursor = 120
            prev_right = None
            first_x = 0

            if count == 0:
                self.canvas.create_text(x_cursor+20, curr_y+10, text="[ Пусто ]", fill="gray", anchor="w")
            else:
                for i in range(count):
                    val = self.logic_module.read_at(struct, i) if self.use_cpp else struct.read_at(i)
                    val_str = str(val)
                    node_w = max(50, node_font.measure(val_str) + 20)
                    hw = node_w / 2
                    
                    x = (prev_right + gap + hw) if prev_right else (x_cursor + hw)
                    if i == 0: first_x = x
                    
                    fill = "#FFFACD" if i == 0 else "#E0F7FA"
                    self.canvas.create_oval(x-hw, curr_y-15, x+hw, curr_y+35, fill=fill, width=2)
                    self.canvas.create_text(x, curr_y+10, text=val_str, font=node_font)
                    self.canvas.create_text(x, curr_y+55, text=f"idx:{i}", font=("Arial", 8), fill="#666")
                    
                    if prev_right:
                        self.canvas.create_line(prev_right, curr_y+10, x-hw, curr_y+10, arrow=tk.LAST)
                    
                    self.nodes_coords.append({'s': s_idx, 'i': i, 'x': x, 'y': curr_y+10, 'hw': hw})
                    prev_right = x + hw
                
                if count > 1:
                    self.canvas.create_arc(first_x, curr_y-100, prev_right-hw, curr_y+80, 
                                           start=0, extent=180, style=tk.ARC, outline="red", dash=(4,2))
                    self.canvas.create_line(first_x, curr_y-15, first_x, curr_y-16, arrow=tk.FIRST, fill="red")
                max_x = max(max_x, prev_right + 100)
            curr_y += 280
        self.canvas.config(scrollregion=(0, 0, max_x, curr_y))

    def add_new_struct(self):
        obj = self.logic_module.create_list() if self.use_cpp else self.logic_module.CyclicLinkedList()
        self.structures.append(obj)
        self.current_idx = len(self.structures) - 1
        self.render(); self.scroll_to_current()

    def remove_current_struct(self):
        if not self.structures: return
        if not messagebox.askyesno("Удаление", f"Удалить структуру {self.current_idx+1}?"): return
        obj = self.structures.pop(self.current_idx)
        if self.use_cpp: self.logic_module.delete_list_obj(obj)
        if not self.structures: self.add_new_struct()
        else: self.current_idx = min(self.current_idx, len(self.structures)-1)
        self.render(); self.scroll_to_current()

    def on_mouse_move(self, event):
        mx, my = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.canvas.delete("del_btn")
        for n in self.nodes_coords:
            if (n['x']-n['hw'] <= mx <= n['x']+n['hw'] and n['y']-25 <= my <= n['y']+25):
                self.canvas.create_oval(n['x']-n['hw'], n['y']-25, n['x']+n['hw'], n['y']+25, fill="#ff4444", tags="del_btn")
                self.canvas.create_text(n['x'], n['y'], text="X", fill="white", font=("Arial", 11, "bold"), tags="del_btn")
                self.canvas.tag_bind("del_btn", "<Button-1>", lambda e, s=n['s'], i=n['i']: self.direct_del(s, i))
                break

    def direct_del(self, s, i):
        struct = self.structures[s]
        if self.use_cpp: self.logic_module.delete_at(struct, i)
        else: struct.delete_at(i)
        self.render()

    def open_dialog(self, cls, *args):
        self.dialog_active = True
        d = cls(self, *args); self.wait_window(d)
        self.dialog_active = False
        return d.result

    def cmd_clear(self):
        s = self.structures[self.current_idx]
        if self.use_cpp: self.logic_module.clear_list(s)
        else: s.clear_list()
        self.render()

    def cmd_add_end(self):
        val = self.open_dialog(SingleValueDialog, "В конец", "Значение:")
        if val is not None:
            s = self.structures[self.current_idx]
            cnt = self.logic_module.get_count(s) if self.use_cpp else s.count
            if self.use_cpp: self.logic_module.insert_at(s, val, cnt)
            else: s.insert_at(val, cnt)
            self.render()

    def cmd_insert(self):
        res = self.open_dialog(InsertDialog)
        if res:
            s = self.structures[self.current_idx]
            if self.use_cpp: self.logic_module.insert_at(s, res[0], res[1])
            else: s.insert_at(res[0], res[1])
            self.render()

    def cmd_read(self):
        idx = self.open_dialog(SingleValueDialog, "Чтение", "Индекс:")
        if idx is not None:
            s = self.structures[self.current_idx]
            v = self.logic_module.read_at(s, idx) if self.use_cpp else s.read_at(idx)
            messagebox.showinfo("Результат", f"Значение: {v}" if v != -1 else "Не найдено")

    def cmd_delete(self):
        idx = self.open_dialog(SingleValueDialog, "Удаление", "Индекс:")
        if idx is not None:
            s = self.structures[self.current_idx]
            if self.use_cpp: self.logic_module.delete_at(s, idx)
            else: s.delete_at(idx)
            self.render()

    def cmd_random(self):
        res = self.open_dialog(RandomDialog)
        if res:
            s = self.structures[self.current_idx]
            if self.use_cpp: self.logic_module.fill_random(s, *res)
            else: s.fill_random(*res)
            self.render()

app = CyclicListGUI()
app.mainloop()