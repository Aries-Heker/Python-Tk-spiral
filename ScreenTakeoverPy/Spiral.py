# Athor Aries-hecker
#Have Fun ;3
import tkinter as tk
import math

# Adjustable parameters:
TIME_INCREMENT = 50     # How much 't' increases each frame (affects spiral growth speed)
SPIRAL_SPACING = 0.05   # Multiplier for 't' to determine the spiral's radius (smaller value = tighter spiral)
ANIMATION_DELAY = 10    # Delay between frames in milliseconds
ROTATION_INCREMENT = 0.01  # How much the whole spiral rotates (in radians) per frame

def on_closing():
    pass  # Prevents closing the window

def animate():
    global t, rotation_offset, points

    # Update time and compute new spiral point in the "local" (unrotated) coordinates.
    t += TIME_INCREMENT
    angle = math.radians(t)
    radius = 1 + SPIRAL_SPACING * t

    # Compute new point (based on polar coordinates with center as origin)
    new_x = center_x + radius * math.cos(angle)
    new_y = center_y + radius * math.sin(angle)
    points.append((new_x, new_y))
    
    # Increment the overall rotation offset.
    rotation_offset += ROTATION_INCREMENT

    # Clear the canvas to redraw the spiral in its rotated state.
    canvas.delete("all")
    
    # Build a new list of points by applying a rotation transformation.
    rotated_points = []
    for x, y in points:
        # Translate the point so that the center is at (0,0)
        rel_x = x - center_x
        rel_y = y - center_y
        # Apply rotation transformation
        rot_x = rel_x * math.cos(rotation_offset) - rel_y * math.sin(rotation_offset)
        rot_y = rel_x * math.sin(rotation_offset) + rel_y * math.cos(rotation_offset)
        # Translate back to the original coordinate system
        final_x = center_x + rot_x
        final_y = center_y + rot_y
        rotated_points.append((final_x, final_y))
    
    # Draw lines connecting each rotated point. Set the spiral color to white and background to black.
    for i in range(1, len(rotated_points)):
        x0, y0 = rotated_points[i-1]
        x1, y1 = rotated_points[i]
        canvas.create_line(x0, y0, x1, y1, fill="white", width=2)  # White spiral color

    # Schedule the next frame.
    canvas.after(ANIMATION_DELAY, animate)

def screenblock():
    global canvas, center_x, center_y, t, points, rotation_offset

    box = tk.Tk()
    box.attributes('-fullscreen', True)  # Fullscreen mode
    box.attributes('-topmost', True)     # Keep window always on top
    box.configure(background='black')    # Set the background to black
    box.protocol("WM_DELETE_WINDOW", on_closing)

    # Remove window borders and title bar
    box.overrideredirect(True)

    # Create a canvas that fills the screen.
    canvas = tk.Canvas(box, width=box.winfo_screenwidth(), height=box.winfo_screenheight(), bg='black', bd=0, highlightthickness=0)  # Black canvas with no border or highlight
    canvas.pack()

    # Set the center of the screen.
    global center_x, center_y
    center_x = box.winfo_screenwidth() / 2
    center_y = box.winfo_screenheight() / 2

    # Initialize our animation variables.
    global t, points, rotation_offset
    t = 0
    points = []          # Stores unrotated spiral points.
    rotation_offset = 0  # Overall rotation angle applied to the spiral.

    animate()  # Start the animation loop.
    box.mainloop()

screenblock()
