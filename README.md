# 2D Geometric Transformations

This project demonstrates 2D geometric transformations (translation, rotation, scaling) using Python with either Tkinter or OpenCV.

## Setup and Installation

1. Ensure you have Python installed (Python 3.6 or higher recommended)
2. Set up a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Three Implementation Options

### Tkinter Version (main.py)

The Tkinter version uses Python's built-in GUI library.

#### Running the Tkinter Version

```
python main.py
```

#### How to Use (Tkinter)

1. **Drawing a Rectangle**:

   - Click and hold the left mouse button
   - Drag to create a rectangle
   - Release the mouse button to complete the rectangle

2. **Applying Transformations**:

   - **Translate**: Click the "Translate" button and enter the x and y displacement values
   - **Rotate**: Click the "Rotate" button and enter the rotation angle in degrees
   - **Scale**: Click the "Scale" button and enter the x and y scaling factors

3. **Reset**: Click the "Reset" button to clear the canvas and start over

### OpenCV Basic Version (opencv_app.py)

A simple OpenCV implementation with command-line inputs.

#### Running the Basic OpenCV Version

```
python opencv_app.py
```

#### How to Use (Basic OpenCV)

1. **Drawing a Rectangle**:

   - Click the "Draw" button (active by default)
   - Click and hold the left mouse button on the canvas
   - Drag to create a rectangle
   - Release the mouse button to complete the rectangle

2. **Applying Transformations**:

   - **Translate**: Click the "Translate" button and enter values in the terminal
   - **Rotate**: Click the "Rotate" button and enter angle in the terminal
   - **Scale**: Click the "Scale" button and enter scaling factors in the terminal

3. **Reset**: Click the "Reset" button to clear the canvas

4. **Quit**: Press 'q' to exit the application

### OpenCV Improved Version (opencv_app_improved.py)

This enhanced version uses OpenCV's GUI capabilities with interactive sliders for parameter adjustments.

#### Running the Improved OpenCV Version

```
python opencv_app_improved.py
```

#### How to Use (Improved OpenCV)

1. **Drawing a Rectangle**:

   - Ensure the Mode slider is set to 0 (Draw mode)
   - Click and hold the left mouse button on the canvas
   - Drag to create a rectangle
   - Release the mouse button to complete the rectangle

2. **Applying Transformations**:

   - Set the Mode slider to the desired transformation:
     - 1: Translation
     - 2: Rotation
     - 3: Scaling
   - Adjust the parameter sliders:
     - For Translation: Adjust "Translate X" and "Translate Y" sliders
     - For Rotation: Adjust "Rotate (degrees)" slider
     - For Scaling: Adjust "Scale X (%)" and "Scale Y (%)" sliders
   - Move the "Apply" slider to 1 to apply the transformation

3. **Reset**: Move the "Reset" slider to 1 to clear the canvas

4. **Quit**: Press 'q' to exit the application

## Features

- White background canvas for drawing
- Interactive rectangle drawing with mouse
- Translation transformation with user-defined parameters
- Rotation transformation with user-defined angle
- Scaling transformation with user-defined factors
- Color-coded transformations for easy visualization
- Cross-platform compatibility

## Why Different Versions?

- **Tkinter**: Simple, built-in library with no external dependencies
- **Basic OpenCV**: Introduction to OpenCV's drawing and transformation capabilities
- **Improved OpenCV**: Demonstrates OpenCV's GUI capabilities with interactive controls, ideal for image processing learning
