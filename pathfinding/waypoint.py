# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 15:17:24 2024

@author: robin
"""

import matplotlib.pyplot as plt
import numpy as np

def circle(radius = 1000, N = 1000): 
    #Center of the circle
    center_x = -radius
    center_y = 0
    # Waypoints generation
    theta = np.linspace(0, 2 * np.pi, N)
    x = center_x + radius * np.cos(theta)
    y = center_y + radius * np.sin(theta)
    waypoints =  (x[::6], y[::6]) 
    return waypoints,x,y,center_x,center_y 

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
    return waypoints, x, y, center_x, center_y

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
    return waypoints, x, y, center_x, center_y