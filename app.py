import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np
import time

# Constants
ml = 150
max_x, max_y = 250 + ml, 50
curr_tool = "Select Tool"
time_init = True
rad = 40
var_inits = False
thick = 7
prevx, prevy = 0, 0

# Get tools function
def getTool(x):
    if x < 50 + ml:
        return "Line"
    elif x < 100 + ml:
        return "Rectangle"
    elif x < 150 + ml:
        return "Draw"
    elif x < 200 + ml:
        return "Circle"
    else:
        return "Erase"

def index_raised(yi, y9):
    if (y9 - yi) > 40:
        return True
    return False

def draw_line(event):
    global prevx, prevy
    x, y = event.x, event.y
    canvas.create_line(prevx, prevy, x, y, fill='black', width=thick)
    prevx, prevy = x, y

def draw_rectangle(event):
    global prevx, prevy
    x, y = event.x, event.y
    canvas.create_rectangle(prevx, prevy, x, y, outline='black', width=thick)

def draw_circle(event):
    global prevx, prevy
    x, y = event.x, event.y
    canvas.create_oval(prevx, prevy, x, y, outline='black', width=thick)

def start_drawing(event):
    global prevx, prevy
    prevx, prevy = event.x, event.y

def erase(event):
    x, y = event.x, event.y
    canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill='white', outline='white')

# Initialize Tkinter window
root = tk.Tk()
root.title("Virtual Painter")

# Create a canvas to display the image
canvas = tk.Canvas(root, width=640, height=480)
canvas.pack()

# Function to update the tool label
def update_tool_label():
    tool_label_text = "Current Tool: " + curr_tool
    tool_label.config(text=tool_label_text)

# Create a label to display the current tool
tool_label = tk.Label(root, text="Current Tool: " + curr_tool)
tool_label.pack()

# Bind drawing events to canvas
canvas.bind("<B1-Motion>", draw_line)
canvas.bind("<ButtonRelease-1>", start_drawing)
canvas.bind("<B3-Motion>", draw_rectangle)
canvas.bind("<B2-Motion>", draw_circle)
canvas.bind("<Shift-B1-Motion>", erase)

# Function to update the GUI
def update_gui():
    update_tool_label()
    root.update()

# Setup webcam
cap = cv2.VideoCapture(0)

# Function to handle window close event
def on_close():
    root.destroy()
    cap.release()

# Bind the close event
root.protocol("WM_DELETE_WINDOW", on_close)

# Main loop
while True:
    _, frm = cap.read()
    frm = cv2.flip(frm, 1)

    # Convert the frame to RGB
    rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)

    # Update the GUI
    update_gui()

    # Show the frame
    cv2.imshow("Virtual Painter", frm)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        cap.release()
        break
