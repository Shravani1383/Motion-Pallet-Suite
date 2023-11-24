from Xlib import X, display

def move_cursor(x, y):
    d = display.Display()
    root = d.screen().root

    # Warp the pointer (cursor) to the specified coordinates
    root.warp_pointer(x, y)
    d.sync()

# Define the target coordinates where you want to move the cursor
x_target = 500
y_target = 500

# Move the cursor to the target coordinates
move_cursor(x_target, y_target)