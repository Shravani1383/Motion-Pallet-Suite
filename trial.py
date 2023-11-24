import cv2
import pytesseract
from PIL import Image, ImageTk
from tkinter import Tk, Canvas, Button, PhotoImage, Label, filedialog
import numpy as np
import threading
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ScribblingTool:
    def __init__(self, root, image_label, canvas):
        self.root = root
        self.image_label = image_label
        self.canvas = canvas
        self.scribble_image = np.ones((500, 500, 3), np.uint8) * 255
        self.scribble_color = (0, 0, 0)

        self.clear_button = Button(root, text="Clear Scribble", command=self.clear_scribble)
        self.clear_button.pack(side="left")

        self.save_button = Button(root, text="Save Scribble", command=self.save_scribble)
        self.save_button.pack(side="left")

        self.convert_button = Button(root, text="Convert", command=self.convert_scribble)
        self.convert_button.pack(side="left")

        self.canvas.bind("<B1-Motion>", self.paint)

    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill="black", width=2, tags="scribble")
        cv2.line(self.scribble_image, (x1, y1), (x2, y2), self.scribble_color, 2)

    def clear_scribble(self):
        self.canvas.delete("scribble")
        self.scribble_image = np.ones((500, 500, 3), np.uint8) * 255

    def save_scribble(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                    filetypes=[("PNG files", "*.png"),
                                                               ("All files", "*.*")])
        cv2.imwrite(file_path, self.scribble_image)

    def convert_scribble(self):
        pil_image = Image.fromarray(cv2.cvtColor(self.scribble_image, cv2.COLOR_BGR2RGB))
        recognized_text = pytesseract.image_to_string(pil_image, config='--psm 6')
        
        # Clear existing text on the canvas
        self.canvas.delete("text")

        # Display the recognized text on the canvas
        self.canvas.create_text(250, 250, text=recognized_text, font=("Helvetica", 12), fill="blue", tags="text")

        # Erase scribble immediately
        self.erase_scribble()

    def erase_scribble(self):
        # Clear only the items with the tag "scribble" on the canvas
        self.canvas.delete("scribble")

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
                                                       ("All files", "*.*")])
    img = cv2.imread(file_path)
    img = cv2.resize(img, (500, 500))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    image_label.config(image=img)
    image_label.image = img
    scribbling_tool.clear_scribble()
    
    

if __name__ == "__main__":
    root = Tk()
    root.title("Scribbling Tool and OCR")

    image_label = Label(root)
    image_label.pack()

    canvas = Canvas(root, width=500, height=500, bg="white")
    canvas.pack()

    open_button = Button(root, text="Open Image", command=open_image)
    open_button.pack()

    scribbling_tool = ScribblingTool(root, image_label, canvas)

    root.mainloop()
