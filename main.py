import tkinter as tk
from tkinter import messagebox, simpledialog
import math

class GeometricTransformationsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("2D Geometric Transformations")
        self.root.geometry("800x600")
        
        # Canvas for drawing
        self.canvas = tk.Canvas(root, bg="white", width=600, height=500)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Control panel
        self.control_panel = tk.Frame(root)
        self.control_panel.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)
        
        # Rectangle coordinates
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.original_coords = None
        
        # Color for rectangle
        self.rect_color = "blue"
        
        # Set up mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        
        # Set up transformation buttons
        self.setup_buttons()
        
    def setup_buttons(self):
        # Heading
        tk.Label(self.control_panel, text="Transformations", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Translation button
        self.translate_btn = tk.Button(self.control_panel, text="Translate", command=self.translate_rectangle)
        self.translate_btn.pack(fill=tk.X, pady=5)
        
        # Rotation button
        self.rotate_btn = tk.Button(self.control_panel, text="Rotate", command=self.rotate_rectangle)
        self.rotate_btn.pack(fill=tk.X, pady=5)
        
        # Scaling button
        self.scale_btn = tk.Button(self.control_panel, text="Scale", command=self.scale_rectangle)
        self.scale_btn.pack(fill=tk.X, pady=5)
        
        # Reset button
        self.reset_btn = tk.Button(self.control_panel, text="Reset", command=self.reset_canvas)
        self.reset_btn.pack(fill=tk.X, pady=20)
    
    def on_mouse_press(self, event):
        self.reset_canvas()
        self.start_x = event.x
        self.start_y = event.y
    
    def on_mouse_drag(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.rect_color)
    
    def on_mouse_release(self, event):
        if self.rect:
            self.original_coords = (self.start_x, self.start_y, event.x, event.y)
            # Enable transformation buttons
            self.translate_btn.config(state=tk.NORMAL)
            self.rotate_btn.config(state=tk.NORMAL)
            self.scale_btn.config(state=tk.NORMAL)
    
    def translate_rectangle(self):
        if not self.original_coords:
            messagebox.showinfo("Error", "Please draw a rectangle first")
            return
        
        dx = simpledialog.askfloat("Translation", "Enter X translation (dx):", parent=self.root)
        if dx is None:
            return
        
        dy = simpledialog.askfloat("Translation", "Enter Y translation (dy):", parent=self.root)
        if dy is None:
            return
        
        x1, y1, x2, y2 = self.original_coords
        # Apply translation
        new_x1, new_y1 = x1 + dx, y1 + dy
        new_x2, new_y2 = x2 + dx, y2 + dy
        
        # Draw translated rectangle in red
        self.canvas.create_rectangle(new_x1, new_y1, new_x2, new_y2, outline="red")
    
    def rotate_rectangle(self):
        if not self.original_coords:
            messagebox.showinfo("Error", "Please draw a rectangle first")
            return
        
        angle = simpledialog.askfloat("Rotation", "Enter rotation angle (in degrees):", parent=self.root)
        if angle is None:
            return
        
        x1, y1, x2, y2 = self.original_coords
        
        # Convert angle to radians
        angle_rad = math.radians(angle)
        
        # Find center of rectangle for rotation
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        
        # Rotate each corner of the rectangle
        new_coords = []
        for x, y in [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]:
            # Translate point to origin
            x_shifted = x - center_x
            y_shifted = y - center_y
            
            # Apply rotation
            new_x = x_shifted * math.cos(angle_rad) - y_shifted * math.sin(angle_rad)
            new_y = x_shifted * math.sin(angle_rad) + y_shifted * math.cos(angle_rad)
            
            # Translate back
            new_x += center_x
            new_y += center_y
            
            new_coords.extend([new_x, new_y])
        
        # Draw rotated rectangle in green
        self.canvas.create_polygon(new_coords, outline="green", fill="")
    
    def scale_rectangle(self):
        if not self.original_coords:
            messagebox.showinfo("Error", "Please draw a rectangle first")
            return
        
        sx = simpledialog.askfloat("Scaling", "Enter X scaling factor (sx):", parent=self.root)
        if sx is None:
            return
        
        sy = simpledialog.askfloat("Scaling", "Enter Y scaling factor (sy):", parent=self.root)
        if sy is None:
            return
        
        x1, y1, x2, y2 = self.original_coords
        
        # Find center of rectangle
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        
        # Calculate new coordinates after scaling
        new_x1 = center_x - (center_x - x1) * sx
        new_y1 = center_y - (center_y - y1) * sy
        new_x2 = center_x + (x2 - center_x) * sx
        new_y2 = center_y + (y2 - center_y) * sy
        
        # Draw scaled rectangle in purple
        self.canvas.create_rectangle(new_x1, new_y1, new_x2, new_y2, outline="purple")
    
    def reset_canvas(self):
        self.canvas.delete("all")
        self.rect = None
        self.original_coords = None
        # Disable transformation buttons
        self.translate_btn.config(state=tk.DISABLED)
        self.rotate_btn.config(state=tk.DISABLED)
        self.scale_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = GeometricTransformationsApp(root)
    root.mainloop() 