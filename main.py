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
        self.root.title("AutoBox Color Clicker")
        self.root.geometry("400x400")
        self.root.resizable(False, False)
        
        # State
        self.selection_region = None # (x, y, w, h)
        self.target_color = None # (r, g, b)
        self.bot = None
        self.is_running = False

        # Styles
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#ccc")
        style.configure("TLabel", font=("Helvetica", 10))
        
        # UI Components
        self.create_widgets()

    def create_widgets(self):
        # Header
        header = ttk.Label(self.root, text="AutoBox Color Clicker", font=("Helvetica", 16, "bold"))
        header.pack(pady=10)

        # Selection Area
        frame_select = ttk.LabelFrame(self.root, text="Target Setup", padding=10)
        frame_select.pack(fill="x", padx=10, pady=5)

        self.btn_new = ttk.Button(frame_select, text="1. New Selection Region", command=self.start_selection)
        self.btn_new.pack(fill="x", pady=5)

        self.lbl_region = ttk.Label(frame_select, text="Region: Not set")
        self.lbl_region.pack(anchor="w")

        # Color Preview
        frame_color = ttk.Frame(frame_select)
        frame_color.pack(fill="x", pady=10)
        
        self.btn_pick_color = ttk.Button(frame_color, text="2. Pick Color", command=self.start_color_pick)
        self.btn_pick_color.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.canvas_color = tk.Canvas(frame_color, width=30, height=30, bg="#eeeeee", highlightthickness=1, highlightbackground="#999")
        self.canvas_color.pack(side="left", padx=5)
        self.lbl_rgb = ttk.Label(frame_color, text="RGB: ---")
        self.lbl_rgb.pack(side="left")

        # Controls
        frame_controls = ttk.LabelFrame(self.root, text="Automation", padding=10)
        frame_controls.pack(fill="x", padx=10, pady=10)

        self.btn_toggle = ttk.Button(frame_controls, text="3. Start", command=self.toggle_bot, state="disabled")
        self.btn_toggle.pack(fill="x", pady=5)

        # Status
        self.lbl_status = ttk.Label(self.root, text="Status: Ready", foreground="gray")
        self.lbl_status.pack(side="bottom", pady=5)

    def start_selection(self):
        self.root.iconify() # Minimize main window
        SelectionOverlay(self.root, self.on_selection_complete)

    def on_selection_complete(self, x, y, w, h):
        self.root.deiconify() # Restore main window
        self.selection_region = (x, y, w, h)
        self.lbl_region.config(text=f"Region: ({x}, {y}) - {w}x{h}")
        self.check_ready()

    def start_color_pick(self):
        self.root.iconify()
        ColorPickerOverlay(self.root, self.on_color_picked)

    def on_color_picked(self, x, y):
        self.root.deiconify()
        try:
            screenshot = pyautogui.screenshot(region=(x, y, 1, 1))
            color = screenshot.getpixel((0, 0))
            self.set_target_color(color)
            self.check_ready()
        except Exception as e:
            self.lbl_status.config(text=f"Error picking color: {e}", foreground="red")

    def set_target_color(self, color):
        self.target_color = color
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
        self.canvas_color.config(bg=hex_color)
        self.lbl_rgb.config(text=f"RGB: {color}")

    def check_ready(self):
        if self.selection_region and self.target_color:
            self.lbl_status.config(text="Ready to start.", foreground="green")
            self.btn_toggle.config(state="normal")
        elif self.selection_region:
             self.lbl_status.config(text="Region set. Now pick a color.", foreground="orange")


    def toggle_bot(self):
        if self.is_running:
            self.stop_bot()
        else:
            self.start_bot()

    def start_bot(self):
        if not self.selection_region or not self.target_color:
            return

        self.is_running = True
        self.btn_toggle.config(text="Stop")
        self.lbl_status.config(text="Running...", foreground="blue")
        self.btn_new.config(state="disabled")
        
        self.bot = ColorClicker(self.selection_region, self.target_color)
        self.bot.start()

    def stop_bot(self):
        self.is_running = False
        self.btn_toggle.config(text="Start")
        self.lbl_status.config(text="Stopped", foreground="gray")
        self.btn_new.config(state="normal")
        
        if self.bot:
            self.bot.stop()
            self.bot = None

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoBoxApp(root)
    root.mainloop()
