import tkinter as tk
from tkinter import Toplevel
from PIL import ImageGrab

class TransparentWindow:
    def __init__(self, master):
        self.master = master
        self.master.geometry('400x300+200+200')  # Default size and position
        self.master.wait_visibility(self.master)
        self.master.attributes('-alpha', 0.3)  # Semi-transparent
        

class StartUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Screen Capture Tool')
        self.master.configure(bg='#333333')  # Dark background

        # Start Capture Button
        self.capture_btn = tk.Button(self.master, text='Capture', command=self.capture_screen, bg='#555555', fg='white')
        self.capture_btn.pack(padx=20, pady=20)

        # Open transparent window button
        self.open_window_btn = tk.Button(self.master, text='Open Window', command=self.open_transparent_window, bg='#555555', fg='white')
        self.open_window_btn.pack(padx=20, pady=20)

        self.transparent_window = None  # Will hold the transparent window

    def open_transparent_window(self):
        # Open the transparent window for selection
        if self.transparent_window is not None:
            self.transparent_window.destroy()

        self.transparent_window = Toplevel(self.master)
        TransparentWindow(self.transparent_window)

    def capture_screen(self):
        if self.transparent_window:
            self.transparent_window.master.overrideredirect(True)
            x1 = self.transparent_window.winfo_x()
            y1 = self.transparent_window.winfo_y()
            x2 = x1 + self.transparent_window.winfo_width()
            y2 = y1 + self.transparent_window.winfo_height()

            # Capture the screen region defined by the transparent window
            img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            # img.save("capture.png")  # Save or handle as needed
            img.show()  # Show the captured image for demonstration
            self.transparent_window.master.overrideredirect(False)
    
    def setActive(self, overlay):
        overlay.lift()
        overlay.focus_force()
        overlay.grab_set()
        overlay.grab_release()

if __name__ == '__main__':
    root = tk.Tk()
    app = StartUI(root)
    root.mainloop()
