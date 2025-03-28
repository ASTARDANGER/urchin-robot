# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import trajectory_generator
import graph_transition
import search_funcs
import math
from gradient_color_generator import colorFader

""" parameters """
search_radius = 0 # how far we search for the next waypoint (impact the quality of trajectory's approximation)
initial_angle = 0 #en degrees
side = 10 #side size of the triangles
 
""" initialization """
## recovery of the waypoints
waypoints,x,y = trajectory_generator.pathFromImg("path.png") ## USER DECIDES OF THE DESIRED PATH HERE
## initialization of the robot position
starting_position = (waypoints[0][0],waypoints[1][0]) ## defined according to the first waypoint
position_list = [starting_position] #list of all the positions taken by the projected barycenter of the robot
state_list = [([1,initial_angle],[3,initial_angle+120],[2,initial_angle+240])] #list of all the angles of the current face
## initialization of the first waypoint
current_waypoint, index_current_waypoint = search_funcs.search_next_waypoint(starting_position, 0, waypoints, search_radius)
i = 0
print(current_waypoint, index_current_waypoint)

""" main """
## main loop
while i < (len(waypoints[0]) - 1): ######TEMPORAIRE
    k=0
    while not search_funcs.point_in_triangle(current_waypoint, position_list[-1], side, state_list[-1])  :
        angle = search_funcs.angle_waypoint(current_waypoint, position_list[-1])
        new_tuple, new_position = graph_transition.transition(state_list[-1], angle, position_list[-1], math.sqrt(3) * side / 2)
        state_list.append(new_tuple)
        position_list.append(new_position)
        k+=1
    last_waypoint, index_last_waypoint = current_waypoint,index_current_waypoint
    current_waypoint, index_current_waypoint = search_funcs.search_next_waypoint(position_list[-1], index_current_waypoint, waypoints, search_radius)
    
    i = index_last_waypoint

""" display """

#triangles = [search_funcs.coord_triangle(position_list[i], side, state_list[i]) for i in range(len(state_list))] ## INUTIL?
## Desired path plot
plt.figure(figsize=(8, 8))
plt.plot(x, y, label="Desired path")
plt.scatter(waypoints[0],waypoints[1], 5, color = "blue", marker="o", label = "Waypoint")
plt.scatter(waypoints[0][0],waypoints[1][0], 20, color = "green", marker="o", label = "Start")
plt.scatter(waypoints[0][-1],waypoints[1][-1], 20, color = "red", marker="o", label = "End")
## Planned path plot with starting and ending triangles
for i in range(len(state_list)) :
    pos_triangle = search_funcs.coord_triangle(position_list[i], side, state_list[i])
    if i ==0 :
        plt.plot([pos_triangle[0][0],pos_triangle[1][0],pos_triangle[2][0],pos_triangle[0][0]],[pos_triangle[0][1],pos_triangle[1][1],pos_triangle[2][1],pos_triangle[0][1]],color ="green")
    elif i == len(state_list)-1 :
        plt.plot([pos_triangle[0][0],pos_triangle[1][0],pos_triangle[2][0],pos_triangle[0][0]],[pos_triangle[0][1],pos_triangle[1][1],pos_triangle[2][1],pos_triangle[0][1]],color ="red")
    else:
        plt.plot([pos_triangle[0][0],pos_triangle[1][0],pos_triangle[2][0],pos_triangle[0][0]],[pos_triangle[0][1],pos_triangle[1][1],pos_triangle[2][1],pos_triangle[0][1]],color =colorFader("green", "red", i/len(state_list)), alpha=0.4)
plt.plot([i[0] for i in position_list], [i[1] for i in position_list],color="red", label="Planned path")
## Graph settings
plt.axhline(0, color="black", linewidth=0.5, linestyle="--")  # x axis
plt.axvline(0, color="black", linewidth=0.5, linestyle="--")  # y axis
plt.gca().set_aspect('equal', adjustable='box')  # same scale on x and y
#plt.xlim(-2100, 200)  # x limits
#plt.ylim(-1200, 1200)  # y limits
plt.title("Path planning of the Urchin Robot")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.grid(True)
plt.show()