# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 16:44:09 2024

@author: robin
"""
import matplotlib.pyplot as plt
import waypoint
import graph_transition
import search_funcs
import math




position = (0,0)
search_radius = 150
angle_initial = 0 #en degrees
a = 150 #coté
liste_position= [position]
liste_etat = [([1,angle_initial],[3,angle_initial+120],[2,angle_initial+240])]
waypoints,x,y,center_x,center_y = waypoint.waypoints_circle()
current_waypoint, index_current_waypoint = search_funcs.search_next_waypoint(position, 0, waypoints, search_radius)
i = 0

print(current_waypoint, index_current_waypoint)
while i < 199: ######TEMPORAIRE
    k=0
    while not search_funcs.point_dans_triangle(current_waypoint, liste_position[-1], a, liste_etat[-1])  :
        angle = search_funcs.angle_waypoint(current_waypoint, liste_position[-1])
        new_tuple, new_position = graph_transition.transition(liste_etat[-1], angle, liste_position[-1], math.sqrt(3) * a / 2)
        liste_etat.append(new_tuple)
        liste_position.append(new_position)
        k+=1
        
       
    
    last_waypoint, index_last_waypoint = current_waypoint,index_current_waypoint
    current_waypoint, index_current_waypoint = search_funcs.search_next_waypoint(liste_position[-1], index_current_waypoint, waypoints, search_radius)
    
    i = index_last_waypoint



print('fini')
triangles = [search_funcs.coord_triangle(liste_position[i], a, liste_etat[i]) for i in range(len(liste_etat))]
# Tracé du cercle
plt.figure(figsize=(8, 8))
plt.plot(x, y, label="Cercle (rayon=1000)")
plt.scatter(waypoints[0],waypoints[1], color = "green", label = "Waypoint")
plt.scatter([center_x], [center_y], color="red", label="Centre (-1000, 0)")
plt.plot([i[0] for i in liste_position], [i[1] for i in liste_position],color="red", label="trajectoire barycentre" )
for i in range(len(liste_etat)) :
    
    pos_triangle = search_funcs.coord_triangle(liste_position[i], a, liste_etat[i])
    if i ==0 :
        plt.plot([pos_triangle[0][0],pos_triangle[1][0],pos_triangle[2][0],pos_triangle[0][0]],[pos_triangle[0][1],pos_triangle[1][1],pos_triangle[2][1],pos_triangle[0][1]],color ="purple")
    elif i == len(liste_etat)-1 :
        plt.plot([pos_triangle[0][0],pos_triangle[1][0],pos_triangle[2][0],pos_triangle[0][0]],[pos_triangle[0][1],pos_triangle[1][1],pos_triangle[2][1],pos_triangle[0][1]],color ="yellow")
    else:
        plt.plot([pos_triangle[0][0],pos_triangle[1][0],pos_triangle[2][0],pos_triangle[0][0]],[pos_triangle[0][1],pos_triangle[1][1],pos_triangle[2][1],pos_triangle[0][1]],color ="blue")
# Configuration de la figure
plt.axhline(0, color="black", linewidth=0.5, linestyle="--")  # Axe des abscisses
plt.axvline(0, color="black", linewidth=0.5, linestyle="--")  # Axe des ordonnées
plt.gca().set_aspect('equal', adjustable='box')  # Assure une échelle égale
plt.xlim(-2100, 200)  # Limites sur l'axe x
plt.ylim(-1200, 1200)  # Limites sur l'axe y
plt.title("Cercle tangent à l'axe des ordonnées")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.grid(True)


# Affichage
plt.show()