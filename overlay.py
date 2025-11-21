import tkinter as tk
import ctypes

def get_virtual_screen_geometry():
    user32 = ctypes.windll.user32
    x = user32.GetSystemMetrics(76) # SM_XVIRTUALSCREEN
    y = user32.GetSystemMetrics(77) # SM_YVIRTUALSCREEN
    w = user32.GetSystemMetrics(78) # SM_CXVIRTUALSCREEN
    h = user32.GetSystemMetrics(79) # SM_CYVIRTUALSCREEN
    return x, y, w, h

class SelectionOverlay:
    def __init__(self, master, on_selection_complete):
        self.master = master
        self.on_selection_complete = on_selection_complete
        
        self.start_x = None
        self.start_y = None
        self.cur_x = None
        self.cur_y = None
        
        # Create a top-level window for the overlay
        self.top = tk.Toplevel(master)
        
        # Multi-monitor support: Use virtual screen geometry instead of fullscreen
        x, y, w, h = get_virtual_screen_geometry()
        self.top.geometry(f"{w}x{h}+{x}+{y}")
        self.top.overrideredirect(True) # Frameless
        
        self.top.attributes('-alpha', 0.3)  # Semi-transparent
        self.top.attributes('-topmost', True)
        self.top.configure(background='black')
        
        # Create a canvas for drawing the selection box
        self.canvas = tk.Canvas(self.top, cursor="cross", bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        
        # Escape to cancel
        self.top.bind("<Escape>", lambda e: self.close())

        self.rect = None

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        # Create the rectangle
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_move_press(self, event):
        self.cur_x, self.cur_y = (event.x, event.y)
        # Update the rectangle
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.cur_x, self.cur_y)

    def on_button_release(self, event):
        if self.start_x is None or self.cur_x is None:
            self.close()
            return

        # Calculate coordinates relative to the canvas (which matches virtual screen)
        x1 = min(self.start_x, self.cur_x)
        y1 = min(self.start_y, self.cur_y)
        x2 = max(self.start_x, self.cur_x)
        y2 = max(self.start_y, self.cur_y)
        
        width = x2 - x1
        height = y2 - y1
        
        # Adjust for virtual screen offset if necessary
        # The event.x/y are relative to the window, which is positioned at virtual x,y.
        # So if the window is at -1920, and event.x is 10, the actual screen x is -1910.
        # However, pyautogui usually expects coordinates relative to the primary monitor (0,0) OR absolute virtual coordinates?
        # Pyautogui handles virtual coordinates fine.
        # We need to pass the absolute screen coordinates.
        
        vx, vy, vw, vh = get_virtual_screen_geometry()
        abs_x = vx + x1
        abs_y = vy + y1
        
        # Ensure we have a valid selection
        if width > 5 and height > 5:
            self.on_selection_complete(abs_x, abs_y, width, height)
        
        self.close()

    def close(self):
        self.top.destroy()

class ColorPickerOverlay:
    def __init__(self, master, on_color_picked):
        self.master = master
        self.on_color_picked = on_color_picked
        
        # Create a top-level window for the overlay
        self.top = tk.Toplevel(master)
        
        # Multi-monitor support
        x, y, w, h = get_virtual_screen_geometry()
        self.top.geometry(f"{w}x{h}+{x}+{y}")
        self.top.overrideredirect(True)
        
        self.top.attributes('-alpha', 0.01)  # Almost invisible but clickable
        self.top.attributes('-topmost', True)
        self.top.configure(cursor="crosshair")
        
        # Bind mouse events
        self.top.bind("<Button-1>", self.on_click)
        self.top.bind("<Escape>", lambda e: self.close())

    def on_click(self, event):
        # event.x_root and y_root are absolute screen coordinates, which is what we want
        x, y = event.x_root, event.y_root
        self.on_color_picked(x, y)
        self.close()

    def close(self):
        self.top.destroy()
