import tkinter as tk
from tkinter import Toplevel, ttk
from PIL import ImageGrab
import pytesseract
import easyocr

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class TransparentWindow:
    def __init__(self, master):
        self.master = master
        self.master.geometry('400x300+200+200')  # Default size and position
        self.master.wait_visibility(self.master)
        # self.master.attributes('-alpha', 0.3)  # Semi-transparent
        self.master.wm_attributes('-transparentcolor', '#ab23ff')
        
        # Create a custom title bar
        title_bar = tk.Frame(self.master, bg='black', relief='raised', bd=2)
        title_bar.pack(fill=tk.X)
        title_bar.bind('<Button-1>', self.start_move)
        title_bar.bind('<ButtonRelease-1>', self.stop_move)
        title_bar.bind('<B1-Motion>', self.on_move)

        # Add a close button to the custom title bar
        close_button = tk.Button(title_bar, text='X', command=self.master.destroy)
        close_button.pack(side=tk.RIGHT)
        
        content = tk.Frame(self.master, bg='#ab23ff', bd=1, highlightbackground="black", highlightthickness=1)
        content.pack(fill=tk.BOTH, expand=True)

    def start_move(self, event):
        global x, y
        x = event.x
        y = event.y

    def stop_move(self, event):
        global x, y
        x = None
        y = None

    def on_move(self, event):
        global x, y
        deltax = event.x - x
        deltay = event.y - y
        x0 = self.master.winfo_x() + deltax
        y0 = self.master.winfo_y() + deltay
        self.master.geometry(f"+{x0}+{y0}")

    def resize(self, event):
        self.master.geometry(f'{event.width}x{event.height}')        

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
        self.transparent_window.overrideredirect(True)
        TransparentWindow(self.transparent_window)

    def capture_screen(self):
        if self.transparent_window:
            self.transparent_window.attributes('-alpha', 0.0)
            x1 = self.transparent_window.winfo_x()
            y1 = self.transparent_window.winfo_y()
            x2 = x1 + self.transparent_window.winfo_width()
            y2 = y1 + self.transparent_window.winfo_height()

            # Capture the screen region defined by the transparent window
            img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            # img.save("capture.png")  # Save or handle as needed
            self.transparent_window.attributes('-alpha', 1.0)

            reader = easyocr.Reader(['ko', 'en'])
            # text = pytesseract.image_to_string(img, lang='kor+eng+jpn')
            text = reader.readtext(img, detail = 0)
            print(text)
    
    def setActive(self, overlay):
        overlay.lift()
        overlay.focus_force()
        overlay.grab_set()
        overlay.grab_release()

if __name__ == '__main__':
    root = tk.Tk()
    app = StartUI(root)
    root.mainloop()
