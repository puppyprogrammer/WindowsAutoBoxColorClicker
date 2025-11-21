import main
import tkinter as tk

# This file (.pyw) will be executed by pythonw.exe automatically on Windows
# preventing the console window from appearing.

if __name__ == "__main__":
    root = tk.Tk()
    app = main.AutoBoxApp(root)
    root.mainloop()
