import tkinter as tk
from tkinter import ttk
import threading
import time
import pyperclip
import pyautogui

class UltimateSpammer:
    def __init__(self, root):
        self.root = root
        self.root.title("终极发送器")
        root.attributes('-topmost', True)

        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        win_w = int(screen_w * 0.5)
        win_h = int(screen_h * 0.6)
        x_pos = screen_w - win_w - 20
        y_pos = 20
        root.geometry(f"{win_w}x{win_h}+{x_pos}+{y_pos}")
        root.minsize(420, 500)
        root.configure(bg='#2c2f33')

        self.running = False
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        self.extreme_mode = tk.BooleanVar(value=False)
        self.fixed_content_mode = tk.BooleanVar(value=False)

        # 样式
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#2c2f33')
        style.configure('TLabel', background='#2c2f33', foreground='white', font=('微软雅黑', 11))
        style.configure('TButton', font=('微软雅黑', 12, 'bold'), borderwidth=0, relief='flat')
        style.map('TButton',
                  background=[('active', '#7289da'), ('!disabled', '#5865f2')],
                  foreground=[('disabled', '#999999')])
        style.configure('Start.TButton', background='#43b581', foreground='white', font=('微软雅黑', 14, 'bold'))
        style.map('Start.TButton',
                  background=[('active', '#3ca374'), ('disabled', '#888')])
        style.configure('Stop.TButton', background='#f04747', foreground='white', font=('微软雅黑', 14, 'bold'))
        style.map('Stop.TButton',
                  background=[('active', '#d84040'), ('disabled', '#888')])
        style.configure('TScale', background='#2c2f33', troughcolor='#40444b', sliderlength=25)
        style.configure('TCheckbutton', background='#2c2f33', foreground='white', font=('微软雅黑', 10))
        style.map('TCheckbutton', background=[('active', '#2c2f33')])
        style.configure('TCombobox', fieldbackground='#40444b', foreground='white', arrowcolor='white')
        style.configure('Warn.TLabel', foreground='#f04747', font=('微软雅黑', 9, 'bold'))

        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 剪贴板预览
        clip_frame = ttk.Frame(main_frame)
        clip_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        self.clip_text = tk.Text(clip_frame, height=6, wrap=tk.WORD, bg='#40444b', fg='white',
                                 font=('Consolas', 14), relief=tk.FLAT, borderwidth=5, padx=10, pady=10)
        self.clip_text.pack(fill=tk.BOTH, expand=True)
        self.clip_text.insert(tk.END, "剪贴板内容预览")

        # 自定义滑块
        slider_frame = ttk.Frame(main_frame)
        slider_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(slider_frame, text="自定义间隔 (秒)").pack(side=tk.LEFT)
        self.speed_var = tk.DoubleVar(value=0.8)
        self.speed_scale = ttk.Scale(
            slider_frame,
            from_=0.0,
            to=3.0,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            length=180,
            command=self.on_scale_change
        )
        self.speed_scale.pack(side=tk.LEFT, padx=10)
        self.speed_label = ttk.Label(slider_frame, text="0.80 秒", width=7)
        self.speed_label.pack(side=tk.LEFT)

        # 极速模式
        extreme_frame = ttk.Frame(main_frame)
        extreme_frame.pack(fill=tk.X, pady=5)
        self.extreme_check = ttk.Checkbutton(
            extreme_frame,
            text="启用极速模式",
            variable=self.extreme_mode,
            command=self.toggle_extreme_mode
        )
        self.extreme_check.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Label(extreme_frame, text="速度档位 ▼").pack(side=tk.LEFT, padx=(0, 5))
        self.speed_combo = ttk.Combobox(
            extreme_frame,
            values=["10条/秒", "20条/秒", "30条/秒", "40条/秒", "50条/秒 (极限)"],
            state="readonly",
            width=14
        )
        self.speed_combo.current(0)
        self.speed_combo.pack(side=tk.LEFT)

        # 固定内容模式
        fix_frame = ttk.Frame(main_frame)
        fix_frame.pack(fill=tk.X, pady=5)
        self.fixed_check = ttk.Checkbutton(
            fix_frame,
            text="固定内容模式（不再读取剪贴板，更快）",
            variable=self.fixed_content_mode
        )
        self.fixed_check.pack(side=tk.LEFT)
        self.toggle_extreme_mode()

        # 警告
        warn_label = ttk.Label(main_frame,
                               text="☠ PAUSE已设为0！50条/秒会瞬间触发封号，测试小号专用 ☠",
                               style='Warn.TLabel', anchor='center')
        warn_label.pack(fill=tk.X, pady=(5, 2))
        warn_label2 = ttk.Label(main_frame, text="开始前务必先点一下聊天输入框",
                                foreground='#faa61a', font=('微软雅黑', 9))
        warn_label2.pack(fill=tk.X, pady=(0, 10))

        # 按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.BOTH, expand=True)
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_rowconfigure(0, weight=1)

        self.start_btn = ttk.Button(btn_frame, text="☢ 开始狂发", style='Start.TButton', command=self.start)
        self.start_btn.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)

        self.stop_btn = ttk.Button(btn_frame, text="❚❚ 紧急停止", style='Stop.TButton', command=self.stop, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=5)

        self.status_label = ttk.Label(main_frame, text="就绪", foreground='#b9bbbe')
        self.status_label.pack(pady=(10, 0))

        self.update_preview()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_scale_change(self, *args):
        val = self.speed_var.get()
        self.speed_label.config(text=f"{val:.2f} 秒")

    def toggle_extreme_mode(self):
        if self.extreme_mode.get():
            self.speed_scale.config(state=tk.DISABLED)
            self.speed_combo.config(state="readonly")
        else:
            self.speed_scale.config(state=tk.NORMAL)
            self.speed_combo.config(state=tk.DISABLED)

    def get_delay(self):
        if self.extreme_mode.get():
            text = self.speed_combo.get()
            num_str = text.split("条")[0]
            try:
                per_sec = int(num_str)
                return 1.0 / per_sec
            except:
                return 0.1
        else:
            return self.speed_var.get()

    def update_preview(self):
        try:
            text = pyperclip.paste()
            self.clip_text.delete(1.0, tk.END)
            self.clip_text.insert(tk.END, text)
        except:
            self.clip_text.delete(1.0, tk.END)
            self.clip_text.insert(tk.END, "读取剪贴板失败")
        self.root.after(300, self.update_preview)

    def start(self):
        with self.lock:
            if self.running:
                return
            if not pyperclip.paste().strip():
                self.status_label.config(text="剪贴板为空", foreground='#f04747')
                return
            self.running = True
            self.stop_event.clear()

        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        mode_text = "极速" if self.extreme_mode.get() else "自定义"
        self.status_label.config(text=f"🔥 {mode_text}发送中… 点击停止", foreground='#f04747')
        threading.Thread(target=self._send_loop, daemon=True).start()

    def stop(self):
        with self.lock:
            self.running = False
            self.stop_event.set()
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="已停止", foreground='#b9bbbe')

    def _send_loop(self):
        # 关键：取消 pyautogui 的默认暂停！
        original_pause = pyautogui.PAUSE
        pyautogui.PAUSE = 0.0

        # 如果开启固定内容模式，只读一次剪贴板
        fixed_msg = None
        if self.fixed_content_mode.get():
            fixed_msg = pyperclip.paste()

        try:
            while self.running:
                # 获取要发送的内容
                if fixed_msg:
                    msg = fixed_msg
                else:
                    msg = pyperclip.paste()

                if msg.strip():
                    pyautogui.hotkey('ctrl', 'v')
                    pyautogui.press('enter')

                delay = self.get_delay()
                if delay <= 0:
                    # 全速时仍保留极短让权，避免界面完全卡死
                    self.stop_event.wait(timeout=0.001)
                else:
                    self.stop_event.wait(timeout=delay)
        except Exception as e:
            print("发送异常:", e)
        finally:
            pyautogui.PAUSE = original_pause   # 恢复默认
            self.root.after(0, lambda: self.status_label.config(text="已停止", foreground='#b9bbbe'))

    def on_close(self):
        self.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateSpammer(root)
    root.mainloop()