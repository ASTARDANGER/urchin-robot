# -*- coding: utf-8 -*-

import math

graph = {(1,3,2) : [(7,1,2), (1,5,3), (2,3,6)],
         (1,5,3) : [(1,3,2), (8,5,1), (3,5,4)],
         (7,1,2) : [(1,3,2), (7,2,9), (8,1,7)],
         (7,2,9) : [(11,7,9), (2,6,9), (7,1,2)],
         (8,1,7) : [(7,1,2), (11,8,7), (8,5,1)],
         (8,5,1) : [(8,1,7), (1,5,3), (12,5,8)],
         (11,8,7) : [(8,1,7), (12,8,11), (11,7,9)],
         (11,7,9) : [(11,8,7), (10,11,9), (7,2,9)],
         (12,8,11) : [(12,5,8), (11,8,7), (10,12,11)],
         (12,5,8) : [(4,5,12), (8,5,1), (12,8,11)],
         (10,12,11) : [(12,8,11), (4,12,10), (10,11,9)],
         (10,11,9) : [(10,12,11), (6,10,9), (11,7,9)],
         (4,12,10) : [(4,5,12),(6,4,10),(10,12,11)],
         (4,5,12) : [(3,5,4), (12,5,8),(4,12,10)],
         (6,4,10) : [(6,10,9),(4,12,10),(3,4,6)],
         (6,10,9) : [(6,4,10),(10,11,9),(2,6,9)],
         (3,4,6) : [(3,5,4),(6,4,10),(2,3,6)],
         (3,5,4) : [(1,5,3), (3,4,6),(4,5,12)],
         (2,3,6) : [(3,4,6), (2,6,9),(1,3,2)],
         (2,6,9) : [(2,3,6),(6,10,9),(7,2,9)]}


def transition(un_tuple, une_direction, current_position, hauteur_triangle) : 
    #contient trois liste de taille 2 avec un sommet et son angle.
    #une_direction contient un angle en degré  
    #la position du centre du triangle 
    #la hauteur du triangle équilatéral
#trouvons entre quel 2 sommet se trouve l'angle direction 
    #programme pour faire ça 
    recherche_sommets = []
    for i in un_tuple : 
        recherche_sommets.append((i[0],min(abs(i[1]-une_direction), 360 -abs(i[1]-une_direction)) )) #on cherche la  diférence entre chaque anglet et une_direction
    def sort_key(e):
        return e[1] 
    recherche_sommets.sort(key=sort_key)#on trie en fontion de la distance d'angle
    for i in range(len(un_tuple)) :
        if un_tuple[i][0] == recherche_sommets[-1][0]:
            dernier_sommet = [i, un_tuple[i][1]]
    #dernier_sommet = [recherche_sommets[-1][0], (recherche_sommets[-1][1]+une_direction)%360] # à la fin du programme on a  le sommet qui n'est pas dans la bonne direction
    liste_des_transitions = graph[(un_tuple[0][0], un_tuple[1][0], un_tuple[2][0])] #on  stocke les transition possible à partir de notre état actuel, mais l graph ne contient pas d'angle
    # programme pour savoir dans liste_des transition quel est le  bon état parmi les 3
    # on regarde celle qui ne contient pas dernier_sommet[0]  
    bonne_transition = ()
    for i in liste_des_transitions : 
        if dernier_sommet[0] not in i :
            bonne_transition = i
    
    # On cherche parmi les 3 sommet de bonne transition lequelle n'est pas dans un_tuple
    un_nouveau_tuple = ( [bonne_transition[0], 0], [bonne_transition[1], 0],[bonne_transition[2], 0])
    un_tuple_simplifie = (un_tuple[0][0],un_tuple[1][0],un_tuple[2][0])
    for i in range(len(un_nouveau_tuple)):     
        if un_nouveau_tuple[i][0] not in un_tuple_simplifie :
            nb_nouveau_sommet = i #la place du nouveau sommet dans bonne_transition
            un_nouveau_tuple[i][1]= (dernier_sommet[1]+180)%360 # son angle est (dernier_sommet[1]+180)%180(modulo?)  
    # On parcours un_nouveau_tuple avec un modulo trois pour assigner des angles à chacun d'entre eux.
    for i in range(len(un_nouveau_tuple)):
        if (nb_nouveau_sommet-i)%3 == 2 : 
            un_nouveau_tuple[i][1] = (un_nouveau_tuple[nb_nouveau_sommet][1]+120)%360
        if (nb_nouveau_sommet-i)%3 == 1 : 
            un_nouveau_tuple[i][1] = (un_nouveau_tuple[nb_nouveau_sommet][1]+240)%360
    # On a un nouveau tuple complet
    #on calcule la nouvelle position du barycentre(aligné avec dernier_sommet)
    new_position = [current_position[0]+hauteur_triangle*2/3*math.cos(math.radians((dernier_sommet[1]+180)%360)),current_position[1]+hauteur_triangle*2/3*math.sin(math.radians((dernier_sommet[1]+180)%360))]
    return un_nouveau_tuple, new_position