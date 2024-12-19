# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 12:04:52 2024

@author: robin
"""

import waypoint
import graph_transition
import math

#r = 300 #reasearch radius to find the next waypoint
#waypoints = waypoint.waypoints_circle()
#position = [0,0]
taille_cote= 150


def search_next_waypoint(position, index_current_waypoint, waypoints,search_radius):
    list_range = [(((position[0]-waypoints[0][i])**2 + (position[1]-waypoints[1][i])**2)**0.5, i) for i in range(len(waypoints[0]))]
    def sort_key(e):
        return e[0] 
    list_range.sort(key = sort_key )
    filtered_index_range = []
    for i in range(len(list_range)) : 
        if list_range[i][0] > search_radius and list_range[i][1] > index_current_waypoint :
            filtered_index_range.append(list_range[i][1])
    if len(filtered_index_range) ==0:
        return [waypoints[0][-1],waypoints[0][-1]],199
    filtered_index_range.sort()
    new_index = filtered_index_range[0]
    
    return [waypoints[0][new_index],waypoints[1][new_index]],new_index


def angle_waypoint(current_waypoint, position):
    dx = current_waypoint[0]-position[0]
    dy = current_waypoint[1]-position[1]
    return math.degrees(math.atan2(dy, dx))%360 # pour l'avoir en degrée(180*2/(2*pi))


# Fonction pour appliquer une rotation à un point autour du barycentre
def rotation(point, angle_deg, centre):
    """Fait tourner un point autour d'un centre donné d'un angle donné (en degrés)."""
    angle_rad = math.radians(angle_deg)
    px, py = point
    cx, cy = centre
    # Translation pour amener le centre à l'origine
    translated_x = px - cx
    translated_y = py - cy
    # Rotation
    rotated_x = translated_x * math.cos(angle_rad) - translated_y * math.sin(angle_rad)
    rotated_y = translated_x * math.sin(angle_rad) + translated_y * math.cos(angle_rad)
    # Revenir à la position initiale
    return (rotated_x + cx, rotated_y + cy)

def coord_triangle(barycentre, a, un_tuple):
    #on commence par trouver le plus petit angle parmi nos 3 sommets
    angles = [i[1] for i in un_tuple] #on récupère les angles 
    angle_deg = min(angles)
    # Coordonnées du barycentre
    bx, by = barycentre
    # Calcul de la hauteur du triangle équilatéral
    h = math.sqrt(3) * a / 2
    # Sommets du triangle avant rotation
    A = (bx+ 2 * h / 3, by) #à droite
    B =( bx - h / 3,by + a / 2) #en haut à gauche
    C =( bx - h / 3,by - a / 2) #en bas à gauche  
    # Appliquer la rotation à chaque sommet autour du barycentre
    A_rot = rotation(A, angle_deg, barycentre)
    B_rot = rotation(B, angle_deg, barycentre)
    C_rot = rotation(C, angle_deg, barycentre) 
    return (A_rot,B_rot,C_rot)

def point_dans_triangle(point, barycentre, a, un_tuple ):
    """
    Vérifie si un point est dans un triangle équilatéral défini par son barycentre, 
    sa longueur de côté et son inclinaison (angle).
    :param point: tuple (x, y) représentant les coordonnées du point à tester.
    :param barycentre: tuple (x, y) représentant les coordonnées du barycentre du triangle.
    :param a: longueur des côtés du triangle.
    :param angle_deg: inclinaison (en degrés) du sommet du triangle par rapport à l'axe vertical.
    :return: True si le point est dans le triangle, False sinon.
    """
    A_rot,B_rot,C_rot = coord_triangle(barycentre, a, un_tuple)
    # Fonction auxiliaire pour calculer le produit vectoriel
    def produit_vectoriel(p1, p2, p3):
        """Produit vectoriel de (p2 - p1) x (p3 - p1)."""
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
    # Vérifie si le point est du même côté pour les trois côtés du triangle
    PA = produit_vectoriel(point,A_rot, B_rot)
    PB = produit_vectoriel(point, B_rot, C_rot)
    PC = produit_vectoriel(point,C_rot, A_rot)
    
    return (PA >= 0 and PB >= 0 and PC >= 0) or (PA <= 0 and PB <= 0 and PC <= 0)



    