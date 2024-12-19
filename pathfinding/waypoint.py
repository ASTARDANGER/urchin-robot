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
    waypoint =  (x[::5], y[::5])
    
    return waypoint,x,y,center_x,center_y 

def square(side=1000, N=1000): ### A REPRENDRE POUR QUE LE TRACE SOIT DANS LE BON ORDRE
    # Center of the square
    center_x = -side / 2
    center_y = 0
    
    # Waypoints generation
    t = np.linspace(0, 1, N)
    # Top edge
    x_top = -side/2 + t * side
    y_top = side/2 * np.ones_like(x_top)
    # Right edge
    x_right = side/2 * np.ones_like(t)
    y_right = side/2 - t * side
    # Bottom edge
    x_bottom = side/2 - t * side
    y_bottom = -side/2 * np.ones_like(x_bottom)
    # Left edge
    x_left = -side/2 * np.ones_like(t)
    y_left = -side/2 + t * side
    # Combine the edges
    x = np.concatenate([x_top, x_right, x_bottom, x_left]) + center_x
    y = np.concatenate([y_top, y_right, y_bottom, y_left]) + center_y
    waypoint = (x[::5], y[::5])
    return waypoint, x, y, center_x, center_y
