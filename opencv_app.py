import cv2
import numpy as np
import math

class GeometricTransformationsApp:
    def __init__(self):
        # Window setup
        self.window_name = "2D Geometric Transformations"
        self.canvas_size = (800, 600)
        self.canvas = np.ones((*self.canvas_size, 3), dtype=np.uint8) * 255  # White canvas
        
        # Rectangle properties
        self.drawing = False
        self.p1 = (-1, -1)
        self.p2 = (-1, -1)
        self.original_rect = None
        self.rect_color = (255, 0, 0)  # Blue in BGR
        
        # Transformation modes
        self.modes = ["Draw", "Translate", "Rotate", "Scale"]
        self.current_mode = "Draw"
        
        # Transformation parameters
        self.dx, self.dy = 0, 0
        self.angle = 0
        self.scale_x, self.scale_y = 1, 1
        
        # UI properties
        self.text_color = (0, 0, 0)  # Black
        self.button_color = (200, 200, 200)
        self.button_hover_color = (150, 150, 150)
        self.button_active_color = (100, 100, 100)
        self.buttons = self._create_buttons()
        
        # Set up mouse callback
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self._mouse_callback)
    
    def _create_buttons(self):
        """Create buttons for mode selection and actions"""
        buttons = []
        y_pos = 20
        for mode in self.modes:
            buttons.append({
                'text': mode,
                'rect': (650, y_pos, 130, 40),
                'action': lambda m=mode: self._set_mode(m)
            })
            y_pos += 50
        
        # Add Reset button
        buttons.append({
            'text': "Reset",
            'rect': (650, y_pos, 130, 40),
            'action': self._reset_canvas
        })
        
        return buttons
    
    def _set_mode(self, mode):
        """Set the current transformation mode"""
        self.current_mode = mode
        if mode == "Translate":
            self._get_translation_params()
        elif mode == "Rotate":
            self._get_rotation_params()
        elif mode == "Scale":
            self._get_scaling_params()
    
    def _get_translation_params(self):
        """Get translation parameters from user"""
        self.dx = int(input("Enter X translation (dx): "))
        self.dy = int(input("Enter Y translation (dy): "))
        self._apply_translation()
    
    def _get_rotation_params(self):
        """Get rotation parameters from user"""
        self.angle = float(input("Enter rotation angle (in degrees): "))
        self._apply_rotation()
    
    def _get_scaling_params(self):
        """Get scaling parameters from user"""
        self.scale_x = float(input("Enter X scaling factor (sx): "))
        self.scale_y = float(input("Enter Y scaling factor (sy): "))
        self._apply_scaling()
    
    def _reset_canvas(self):
        """Reset the canvas to its initial state"""
        self.canvas = np.ones((*self.canvas_size, 3), dtype=np.uint8) * 255
        self.drawing = False
        self.p1 = (-1, -1)
        self.p2 = (-1, -1)
        self.original_rect = None
        self.current_mode = "Draw"
        self._draw_ui()
    
    def _mouse_callback(self, event, x, y, flags, param):
        """Handle mouse events"""
        if self.current_mode == "Draw":
            if event == cv2.EVENT_LBUTTONDOWN:
                self.drawing = True
                self.p1 = (x, y)
            
            elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
                # Create a copy of the canvas to draw temporary rectangle
                temp_canvas = self.canvas.copy()
                cv2.rectangle(temp_canvas, self.p1, (x, y), self.rect_color, 2)
                self._draw_ui(temp_canvas)
                cv2.imshow(self.window_name, temp_canvas)
            
            elif event == cv2.EVENT_LBUTTONUP and self.drawing:
                self.drawing = False
                self.p2 = (x, y)
                self.original_rect = [self.p1, self.p2]
                # Draw the rectangle on the canvas
                cv2.rectangle(self.canvas, self.p1, self.p2, self.rect_color, 2)
                self._draw_ui()
        
        # Check button clicks
        if event == cv2.EVENT_LBUTTONDOWN:
            for button in self.buttons:
                bx, by, bw, bh = button['rect']
                if bx <= x <= bx + bw and by <= y <= by + bh:
                    button['action']()
    
    def _apply_translation(self):
        """Apply translation transformation to the rectangle"""
        if self.original_rect:
            p1, p2 = self.original_rect
            # Calculate new coordinates after translation
            new_p1 = (p1[0] + self.dx, p1[1] + self.dy)
            new_p2 = (p2[0] + self.dx, p2[1] + self.dy)
            
            # Draw translated rectangle (red)
            cv2.rectangle(self.canvas, new_p1, new_p2, (0, 0, 255), 2)
            self._draw_ui()
    
    def _apply_rotation(self):
        """Apply rotation transformation to the rectangle"""
        if self.original_rect:
            p1, p2 = self.original_rect
            
            # Calculate center of the rectangle
            center_x = (p1[0] + p2[0]) // 2
            center_y = (p1[1] + p2[1]) // 2
            center = (center_x, center_y)
            
            # Calculate corners of the rectangle
            corners = [
                p1,
                (p2[0], p1[1]),
                p2,
                (p1[0], p2[1])
            ]
            
            # Create rotation matrix
            angle_rad = math.radians(self.angle)
            cos_theta = math.cos(angle_rad)
            sin_theta = math.sin(angle_rad)
            
            # Apply rotation to each corner
            rotated_corners = []
            for x, y in corners:
                # Translate point to origin
                x_shifted = x - center[0]
                y_shifted = y - center[1]
                
                # Apply rotation
                new_x = x_shifted * cos_theta - y_shifted * sin_theta
                new_y = x_shifted * sin_theta + y_shifted * cos_theta
                
                # Translate back
                new_x += center[0]
                new_y += center[1]
                
                rotated_corners.append((int(new_x), int(new_y)))
            
            # Draw rotated rectangle (green)
            points = np.array(rotated_corners, np.int32)
            points = points.reshape((-1, 1, 2))
            cv2.polylines(self.canvas, [points], True, (0, 255, 0), 2)
            self._draw_ui()
    
    def _apply_scaling(self):
        """Apply scaling transformation to the rectangle"""
        if self.original_rect:
            p1, p2 = self.original_rect
            
            # Calculate center of the rectangle
            center_x = (p1[0] + p2[0]) // 2
            center_y = (p1[1] + p2[1]) // 2
            
            # Calculate new coordinates after scaling
            new_p1_x = center_x - (center_x - p1[0]) * self.scale_x
            new_p1_y = center_y - (center_y - p1[1]) * self.scale_y
            new_p2_x = center_x + (p2[0] - center_x) * self.scale_x
            new_p2_y = center_y + (p2[1] - center_y) * self.scale_y
            
            new_p1 = (int(new_p1_x), int(new_p1_y))
            new_p2 = (int(new_p2_x), int(new_p2_y))
            
            # Draw scaled rectangle (purple)
            cv2.rectangle(self.canvas, new_p1, new_p2, (255, 0, 255), 2)
            self._draw_ui()
    
    def _draw_ui(self, canvas=None):
        """Draw UI elements on the canvas"""
        if canvas is None:
            canvas = self.canvas
        
        # Draw buttons
        for button in self.buttons:
            x, y, w, h = button['rect']
            color = self.button_active_color if button['text'] == self.current_mode else self.button_color
            cv2.rectangle(canvas, (x, y), (x + w, y + h), color, -1)
            cv2.rectangle(canvas, (x, y), (x + w, y + h), (0, 0, 0), 1)
            
            # Calculate text position for centering
            text_size = cv2.getTextSize(button['text'], cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
            text_x = x + (w - text_size[0]) // 2
            text_y = y + (h + text_size[1]) // 2
            
            cv2.putText(canvas, button['text'], (text_x, text_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        
        # Draw current mode info
        cv2.putText(canvas, f"Mode: {self.current_mode}", (20, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.text_color, 2, cv2.LINE_AA)
        
        # Update display
        cv2.imshow(self.window_name, canvas)
    
    def run(self):
        """Run the application main loop"""
        self._reset_canvas()
        
        while True:
            self._draw_ui()
            key = cv2.waitKey(1) & 0xFF
            
            # Exit on 'q' key
            if key == ord('q'):
                break
        
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = GeometricTransformationsApp()
    app.run() 