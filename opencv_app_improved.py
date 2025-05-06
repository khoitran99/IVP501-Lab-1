import cv2
import numpy as np
import math

class GeometricTransformationsApp:
    def __init__(self):
        # Window setup
        self.window_name = "2D Geometric Transformations"
        self.canvas_size = (800, 600)
        self.canvas = np.ones((*self.canvas_size, 3), dtype=np.uint8) * 255  # White canvas
        self.base_canvas = self.canvas.copy()  # Store for reset
        
        # Control panel
        self.control_panel_name = "Controls"
        cv2.namedWindow(self.control_panel_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.control_panel_name, 400, 200)
        
        # Rectangle properties
        self.drawing = False
        self.p1 = (-1, -1)
        self.p2 = (-1, -1)
        self.original_rect = None
        self.rect_color = (255, 0, 0)  # Blue in BGR
        
        # Transformation parameters
        self.dx, self.dy = 0, 0
        self.angle = 0
        self.scale_x, self.scale_y = 1, 1
        
        # Set up mouse callback
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self._mouse_callback)
        
        # Modes
        self.DRAW_MODE = 0
        self.TRANSLATE_MODE = 1
        self.ROTATE_MODE = 2
        self.SCALE_MODE = 3
        self.current_mode = self.DRAW_MODE
        
        # Create control panel
        self._create_control_panel()
    
    def _create_control_panel(self):
        """Create sliders and buttons in the control panel"""
        # Mode selection trackbar
        cv2.createTrackbar("Mode", self.control_panel_name, self.current_mode, 3, self._on_mode_change)
        
        # Translation parameters
        cv2.createTrackbar("Translate X", self.control_panel_name, 50, 100, self._on_translate_x_change)
        cv2.createTrackbar("Translate Y", self.control_panel_name, 50, 100, self._on_translate_y_change)
        
        # Rotation parameter
        cv2.createTrackbar("Rotate (degrees)", self.control_panel_name, 0, 360, self._on_rotation_change)
        
        # Scaling parameters
        cv2.createTrackbar("Scale X (%)", self.control_panel_name, 100, 200, self._on_scale_x_change)
        cv2.createTrackbar("Scale Y (%)", self.control_panel_name, 100, 200, self._on_scale_y_change)
        
        # Apply button is simulated with mode selection
        cv2.createTrackbar("Apply", self.control_panel_name, 0, 1, self._on_apply)
        
        # Reset button is simulated with trackbar
        cv2.createTrackbar("Reset", self.control_panel_name, 0, 1, self._on_reset)
    
    def _on_mode_change(self, value):
        """Handle mode change from trackbar"""
        self.current_mode = value
        # Reset apply button if mode changes
        cv2.setTrackbarPos("Apply", self.control_panel_name, 0)
    
    def _on_translate_x_change(self, value):
        """Handle translation X change"""
        self.dx = value - 50  # Center at 0 (50 in trackbar)
    
    def _on_translate_y_change(self, value):
        """Handle translation Y change"""
        self.dy = value - 50  # Center at 0 (50 in trackbar)
    
    def _on_rotation_change(self, value):
        """Handle rotation angle change"""
        self.angle = value
    
    def _on_scale_x_change(self, value):
        """Handle scale X change"""
        self.scale_x = value / 100.0  # Convert percentage to factor
    
    def _on_scale_y_change(self, value):
        """Handle scale Y change"""
        self.scale_y = value / 100.0  # Convert percentage to factor
    
    def _on_apply(self, value):
        """Apply the current transformation when trackbar changes to 1"""
        if value == 1:
            if self.current_mode == self.TRANSLATE_MODE:
                self._apply_translation()
            elif self.current_mode == self.ROTATE_MODE:
                self._apply_rotation()
            elif self.current_mode == self.SCALE_MODE:
                self._apply_scaling()
            # Reset apply button to 0 automatically
            cv2.setTrackbarPos("Apply", self.control_panel_name, 0)
    
    def _on_reset(self, value):
        """Reset canvas when trackbar changes to 1"""
        if value == 1:
            self._reset_canvas()
            # Reset the trackbar to 0 automatically
            cv2.setTrackbarPos("Reset", self.control_panel_name, 0)
    
    def _mouse_callback(self, event, x, y, flags, param):
        """Handle mouse events"""
        if self.current_mode == self.DRAW_MODE:
            if event == cv2.EVENT_LBUTTONDOWN:
                self.drawing = True
                self.p1 = (x, y)
                # Store current canvas for rectangle drawing
                self.base_canvas = self.canvas.copy()
            
            elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
                # Create a copy of the base canvas to draw temporary rectangle
                temp_canvas = self.base_canvas.copy()
                cv2.rectangle(temp_canvas, self.p1, (x, y), self.rect_color, 2)
                cv2.imshow(self.window_name, temp_canvas)
            
            elif event == cv2.EVENT_LBUTTONUP and self.drawing:
                self.drawing = False
                self.p2 = (x, y)
                self.original_rect = [self.p1, self.p2]
                # Draw the rectangle on the canvas
                self.canvas = self.base_canvas.copy()
                cv2.rectangle(self.canvas, self.p1, self.p2, self.rect_color, 2)
                cv2.imshow(self.window_name, self.canvas)
    
    def _apply_translation(self):
        """Apply translation transformation to the rectangle"""
        if self.original_rect:
            p1, p2 = self.original_rect
            # Calculate new coordinates after translation
            new_p1 = (p1[0] + self.dx, p1[1] + self.dy)
            new_p2 = (p2[0] + self.dx, p2[1] + self.dy)
            
            # Create a copy of the current canvas
            temp_canvas = self.canvas.copy()
            
            # Draw translated rectangle (red)
            cv2.rectangle(temp_canvas, new_p1, new_p2, (0, 0, 255), 2)
            self.canvas = temp_canvas
            cv2.imshow(self.window_name, self.canvas)
    
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
            
            # Create a copy of the current canvas
            temp_canvas = self.canvas.copy()
            
            # Apply OpenCV rotation matrix for more accurate rotation
            angle_rad = math.radians(self.angle)
            
            # Apply rotation to each corner
            rotated_corners = []
            for x, y in corners:
                # Use OpenCV's rotation function
                rotation_matrix = cv2.getRotationMatrix2D(center, self.angle, 1)
                pt = np.array([[x], [y], [1]])
                rotated_pt = np.dot(rotation_matrix, pt)
                rotated_corners.append((int(rotated_pt[0][0]), int(rotated_pt[1][0])))
            
            # Draw rotated rectangle (green)
            points = np.array(rotated_corners, np.int32)
            points = points.reshape((-1, 1, 2))
            cv2.polylines(temp_canvas, [points], True, (0, 255, 0), 2)
            self.canvas = temp_canvas
            cv2.imshow(self.window_name, self.canvas)
    
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
            
            # Create a copy of the current canvas
            temp_canvas = self.canvas.copy()
            
            # Draw scaled rectangle (purple)
            cv2.rectangle(temp_canvas, new_p1, new_p2, (255, 0, 255), 2)
            self.canvas = temp_canvas
            cv2.imshow(self.window_name, self.canvas)
    
    def _reset_canvas(self):
        """Reset the canvas to its initial state"""
        self.canvas = np.ones((*self.canvas_size, 3), dtype=np.uint8) * 255
        self.base_canvas = self.canvas.copy()
        self.drawing = False
        self.p1 = (-1, -1)
        self.p2 = (-1, -1)
        self.original_rect = None
        
        # Reset parameters
        self.dx, self.dy = 0, 0
        self.angle = 0
        self.scale_x, self.scale_y = 1, 1
        
        # Reset trackbars
        cv2.setTrackbarPos("Mode", self.control_panel_name, self.DRAW_MODE)
        cv2.setTrackbarPos("Translate X", self.control_panel_name, 50)
        cv2.setTrackbarPos("Translate Y", self.control_panel_name, 50)
        cv2.setTrackbarPos("Rotate (degrees)", self.control_panel_name, 0)
        cv2.setTrackbarPos("Scale X (%)", self.control_panel_name, 100)
        cv2.setTrackbarPos("Scale Y (%)", self.control_panel_name, 100)
        
        # Update display
        cv2.imshow(self.window_name, self.canvas)
    
    def run(self):
        """Run the application main loop"""
        # First display
        cv2.imshow(self.window_name, self.canvas)
        
        print("=== 2D Geometric Transformations with OpenCV ===")
        print("Instructions:")
        print("1. Select 'Draw' mode (0) and draw a rectangle")
        print("2. Select a transformation mode:")
        print("   - Translate (1): Adjust X and Y sliders")
        print("   - Rotate (2): Adjust rotation angle slider")
        print("   - Scale (3): Adjust X and Y scaling sliders")
        print("3. Click 'Apply' slider to apply transformation")
        print("4. Click 'Reset' slider to clear the canvas")
        print("5. Press 'q' to quit")
        
        while True:
            key = cv2.waitKey(1) & 0xFF
            
            # Exit on 'q' key
            if key == ord('q'):
                break
        
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = GeometricTransformationsApp()
    app.run() 