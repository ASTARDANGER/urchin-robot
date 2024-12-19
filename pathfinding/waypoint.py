# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 15:17:24 2024

@author: robin
"""

import matplotlib.pyplot as plt
import numpy as np


def waypoints_circle() : 
    # Rayon du cercle
    radius = 1000
    
    # Centre du cercle (à gauche de l'axe des ordonnées)
    center_x = -radius
    center_y = 0
    
    # Génération des points du cercle
    theta = np.linspace(0, 2 * np.pi, 1000)  # Angle de 0 à 2π en 1000 points
    x = center_x + radius * np.cos(theta)    # Coordonnées x
    y = center_y + radius * np.sin(theta)    # Coordonnées y
    waypoint =  (x[::5], y[::5])
    
    
    return waypoint,x,y,center_x,center_y 



    





# Affichage
plt.show()
