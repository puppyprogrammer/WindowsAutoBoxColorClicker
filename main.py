import tkinter as tk
from tkinter import ttk
import pyautogui
from overlay import SelectionOverlay, ColorPickerOverlay
from bot import ColorClicker
import threading
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()


class AutoBoxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoBox Matrix v2.0")
        self.root.geometry("500x600")
        self.root.resizable(True, True)
        
        # Theme Colors
        self.bg_color = "#000000"
        self.fg_color = "#00FF00" # Matrix Green
        self.accent_color = "#003300"
        
        self.root.configure(bg=self.bg_color)
        
        # State
        self.targets = [] # List of dicts: {'region': (x,y,w,h), 'color': (r,g,b)}
        self.temp_region = None
        self.bot = None
        self.is_running = False

        # Styles
        self.setup_styles()
        
        # UI Components
        self.create_widgets()

        # Bindings
        self.root.bind('<Escape>', self.pause_bot)
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('default')
        
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=("Consolas", 10))
        style.configure("TLabelframe", background=self.bg_color, foreground=self.fg_color, bordercolor=self.fg_color)
        style.configure("TLabelframe.Label", background=self.bg_color, foreground=self.fg_color, font=("Consolas", 10, "bold"))
        
        style.configure("TButton", 
                        background=self.accent_color, 
                        foreground=self.fg_color, 
                        font=("Consolas", 10, "bold"),
                        borderwidth=1,
                        focuscolor=self.fg_color)
        style.map("TButton", background=[('active', self.fg_color)], foreground=[('active', self.bg_color)])
        
        style.configure("TSpinbox", fieldbackground=self.bg_color, foreground=self.fg_color, arrowcolor=self.fg_color)

    def create_widgets(self):
        # Header
        header = ttk.Label(self.root, text="[ SYSTEM ONLINE ]", font=("Consolas", 16, "bold"))
        header.pack(pady=15)

        # Target List Area
        frame_list = ttk.LabelFrame(self.root, text="Active Targets", padding=10)
        frame_list.pack(fill="both", expand=True, padx=10, pady=5)

        # Listbox with Scrollbar
        self.list_targets = tk.Listbox(frame_list, 
                                       bg=self.bg_color, 
                                       fg=self.fg_color, 
                                       font=("Consolas", 9), 
                                       selectbackground=self.fg_color, 
                                       selectforeground=self.bg_color,
                                       highlightthickness=1,
                                       highlightbackground=self.fg_color,
                                       relief="flat")
        self.list_targets.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(frame_list, orient="vertical", command=self.list_targets.yview)
        scrollbar.pack(side="right", fill="y")
        self.list_targets.config(yscrollcommand=scrollbar.set)

        # Target Controls
        frame_target_btns = ttk.Frame(self.root)
        frame_target_btns.pack(fill="x", padx=10, pady=5)
        
        btn_style = {
            "bg": self.accent_color,
            "fg": self.fg_color,
            "font": ("Consolas", 10, "bold"),
            "relief": "flat",
            "activebackground": self.fg_color,
            "activeforeground": self.bg_color,
            "cursor": "hand2"
        }
        
        self.btn_add = tk.Button(frame_target_btns, text="+ ADD TARGET", command=self.start_add_target_flow, **btn_style)
        self.btn_add.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.btn_del = tk.Button(frame_target_btns, text="- REMOVE SELECTED", command=self.remove_target, **btn_style)
        self.btn_del.pack(side="left", fill="x", expand=True, padx=(5, 0))

        # Main Controls
        frame_controls = ttk.LabelFrame(self.root, text="Command Console", padding=10)
        frame_controls.pack(fill="x", padx=10, pady=10)

        # Delay Input
        frame_delay = ttk.Frame(frame_controls)
        frame_delay.pack(fill="x", pady=(0, 10))
        ttk.Label(frame_delay, text="SCAN_DELAY(s):").pack(side="left")
        self.var_delay = tk.DoubleVar(value=0.1)
        self.spin_delay = ttk.Spinbox(frame_delay, from_=0.0, to=10.0, increment=0.1, textvariable=self.var_delay, width=5)
        self.spin_delay.pack(side="left", padx=10)

        self.btn_toggle = tk.Button(frame_controls, text="START", command=self.toggle_bot, **btn_style)
        self.btn_toggle.pack(fill="x", pady=5)

        # Status
        self.lbl_status = ttk.Label(self.root, text="STATUS: IDLE", foreground=self.fg_color)
        self.lbl_status.pack(side="bottom", pady=5)

    def start_add_target_flow(self):
        self.lbl_status.config(text="STATUS: SELECT REGION...")
        self.root.iconify()
        SelectionOverlay(self.root, self.on_region_selected)

    def on_region_selected(self, x, y, w, h):
        self.temp_region = (x, y, w, h)
        # Immediately start color pick
        self.root.deiconify() # Briefly show to handle focus if needed, but better to stay hidden or re-hide
        # Actually, let's keep it hidden or re-hide for smooth flow
        # But we need to update status? 
        # Let's just go straight to color picker
        self.lbl_status.config(text="STATUS: PICK COLOR...")
        ColorPickerOverlay(self.root, self.on_color_picked)

    def on_color_picked(self, x, y):
        self.root.deiconify()
        try:
            screenshot = pyautogui.screenshot(region=(x, y, 1, 1))
            color = screenshot.getpixel((0, 0))
            
            # Add to targets
            target = {'region': self.temp_region, 'color': color}
            self.targets.append(target)
            
            # Update Listbox
            self.update_listbox()
            self.lbl_status.config(text="STATUS: TARGET ACQUIRED")
            
        except Exception as e:
            self.lbl_status.config(text=f"ERROR: {e}")

    def update_listbox(self):
        self.list_targets.delete(0, tk.END)
        for i, t in enumerate(self.targets):
            r = t['region']
            c = t['color']
            self.list_targets.insert(tk.END, f"[{i+1}] Region: {r} | Color: {c}")

    def remove_target(self):
        selection = self.list_targets.curselection()
        if selection:
            index = selection[0]
            del self.targets[index]
            self.update_listbox()
            self.lbl_status.config(text="STATUS: TARGET REMOVED")

    def toggle_bot(self):
        if self.is_running:
            self.stop_bot()
        else:
            self.start_bot()

    def start_bot(self):
        if not self.targets:
            self.lbl_status.config(text="ERROR: NO TARGETS")
            return

        self.is_running = True
        self.btn_toggle.config(text="STOP")
        self.lbl_status.config(text="STATUS: RUNNING...")
        self.btn_add.config(state="disabled")
        self.btn_del.config(state="disabled")
        self.spin_delay.config(state="disabled")
        
        try:
            delay = float(self.var_delay.get())
        except ValueError:
            delay = 0.1

        self.bot = ColorClicker(self.targets, delay=delay)
        self.bot.start()

    def stop_bot(self):
        self.is_running = False
        self.btn_toggle.config(text="START")
        self.lbl_status.config(text="STATUS: PAUSED")
        self.btn_add.config(state="normal")
        self.btn_del.config(state="normal")
        self.spin_delay.config(state="normal")
        
        if self.bot:
            self.bot.stop()
            self.bot = None

    def pause_bot(self, event=None):
        if self.is_running:
            self.stop_bot()

    def quit_app(self, event=None):
        self.stop_bot()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoBoxApp(root)
    root.mainloop()
