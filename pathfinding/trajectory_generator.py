# -*- coding: utf-8 -*-

import numpy as np
from skimage import io, color
from scipy.interpolate import splprep, splev
"""
import matplotlib.pyplot as plt
import matplotlib.colors as mplcolors
## to plot with a gradient of color
def colorFader(c1="green",c2="red",mix=0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    c1=np.array(mplcolors.to_rgb(c1))
    c2=np.array(mplcolors.to_rgb(c2))
    return mplcolors.to_hex((1-mix)*c1 + mix*c2)
"""

def circle(radius = 1000, N = 1000): 
    #Center of the circle
    center_x = -radius
    center_y = 0
    # Waypoints generation
    theta = np.linspace(0, 2 * np.pi, N)
    x = center_x + radius * np.cos(theta)
    y = center_y + radius * np.sin(theta)
    waypoints =  (x[::6], y[::6]) 
    return waypoints,x,y 

def square(side=2000, N=1000):
    # Center of the square
    center_x = 0
    center_y = 0
    # Waypoints generation
    N_per_edge = N // 4  # Divide points equally among four edges
    # Top edge (left to right)
    x_top = np.linspace(-side/2, side/2, N_per_edge)
    y_top = np.full_like(x_top, side/2)
    # Right edge (top to bottom)
    y_right = np.linspace(side/2, -side/2, N_per_edge)
    x_right = np.full_like(y_right, side/2)
    # Bottom edge (right to left)
    x_bottom = np.linspace(side/2, -side/2, N_per_edge)
    y_bottom = np.full_like(x_bottom, -side/2)
    # Left edge (bottom to top)
    y_left = np.linspace(-side/2, side/2, N_per_edge)
    x_left = np.full_like(y_left, -side/2)
    # Combine edges in a continuous path
    x = np.concatenate([x_top, x_right, x_bottom, x_left]) + center_x
    y = np.concatenate([y_top, y_right, y_bottom, y_left]) + center_y
    waypoints = (x[::5], y[::5])
    return waypoints, x, y

def pentagon(side=2000, N=1000):
    # Center of the pentagon
    center_x = 0
    center_y = 0
    # Calculate the radius of the circumscribed circle
    radius = side / (2 * np.sin(np.pi / 5))
    # Angles of the vertices of the pentagon
    angles = np.linspace(0, 2 * np.pi, 6)[:-1]  # 5 points, closing the shape by excluding the last point
    # Vertices of the pentagon
    x_vertices = center_x + radius * np.cos(angles + np.pi / 2)  # Rotate to align top vertex with y-axis
    y_vertices = center_y + radius * np.sin(angles + np.pi / 2)
    # Distribute points along the edges
    points_per_edge = N // 5
    x = []
    y = []
    for i in range(5):
        x_edge = np.linspace(x_vertices[i], x_vertices[(i + 1) % 5], points_per_edge, endpoint=False)
        y_edge = np.linspace(y_vertices[i], y_vertices[(i + 1) % 5], points_per_edge, endpoint=False)
        x.append(x_edge)
        y.append(y_edge)
    # Combine the edges in a continuous path
    x = np.concatenate(x)
    y = np.concatenate(y)
    waypoints = (x[::5], y[::5])
    return waypoints, x, y

## Function to find a path following all black pixels in an image
def pathFromImg(image_path, num_points=500):
    # Load the image
    image = io.imread(image_path)
    # Check for RGBA images and convert to RGB if needed
    if image.shape[-1] == 4:  # RGBA
        image = image[:, :, :3]

    # Detect start (green) and end (red) pixels
    start_pixel = np.argwhere((image == [0, 255, 0]).all(axis=2))
    if len(start_pixel) == 0:
        raise ValueError("Start point not found in the image.")
    start_point = start_pixel[0]
    #end_pixel = np.argwhere((image == [255, 0, 0]).all(axis=2))
    #if len(end_pixel) == 0:
    #    raise ValueError("End point not found in the image.")
    #end_point = end_pixel[0]

    # Convert image to grayscale and detect black pixels
    image_gray = color.rgb2gray(image)
    black_pixels = np.argwhere(image_gray < 0.1)
    if len(black_pixels) == 0:
        raise ValueError("No black pixels detected in the image.")
    
    # Reorder black pixels to construct a continuous path
    path = [start_point]
    remaining_pixels = set(map(tuple, black_pixels)) # Convert to set of tuples for faster removal
    remaining_pixels.discard(tuple(start_point)) # We store every black pixel except the start pixel
    current_point = start_point
    while remaining_pixels:
        nearest_pixel = min(remaining_pixels, key=lambda p: np.linalg.norm(np.array(p) - current_point))
        path.append(nearest_pixel)
        remaining_pixels.remove(nearest_pixel)
        current_point = nearest_pixel
    path = np.array(path)

    # We have a path, now we interpolate it to get more points and a smoothed curve
    tck = splprep([path[:, 1], image.shape[0]-path[:, 0]], s=len(path[:, 1]))[0] #image.shape[0] - path[:, 0] to invert y axis
    u = np.linspace(0, 1, num_points)
    x, y = splev(u, tck)
    """ 
    ## Visualization
    plt.figure(figsize=(10, 10))
    # Show the image
    plt.imshow(image, origin='upper') 
    # Show the detected path
    plt.plot(path[:, 1], path[:, 0], 'blue', label="Detected Path") 
    # Show the interpolated points
    for i in range(len(x)):
        plt.scatter(x[i], y[i], color=colorFader("darkblue", "lightblue", i/len(x)), s=20) 
    # Show the start and end points
    plt.scatter(start_point[1], start_point[0], color='green', label="Start", s=50)
    plt.scatter(end_point[1], end_point[0], color='red', label="End", s=50)
    # Graph settings
    plt.legend()
    plt.axis('off')
    plt.title("Path Following All Black Pixels")
    plt.show()
    """
    # We return the waypoints as a numpy array and the x, y coordinates
    print(x)
    waypoints = (x[::3], y[::3])
    return waypoints, x, y