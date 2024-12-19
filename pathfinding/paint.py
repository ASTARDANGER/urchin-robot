# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 12:28:13 2024

@author: robin
"""

import cv2
import numpy as np

from scipy.interpolate import splprep, splev
import matplotlib.pyplot as plt

def extract_trajectory_from_image(image_path):
    # Charger l'image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Impossible de charger l'image : {image_path}")
    
    # Convertir en niveaux de gris
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Appliquer un seuil pour binariser l'image
    _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Trouver les contours du tracé
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) == 0:
        raise ValueError("Aucun contour détecté. Assurez-vous que l'image contient un tracé visible.")

    # Sélectionner le plus grand contour (au cas où il y en aurait plusieurs)
    contour = max(contours, key=cv2.contourArea)
    
    # Extraire les points du contour
    trajectory = [(point[0][0], point[0][1]) for point in contour]
    
    return trajectory

def generate_constant_step_points(trajectory, step_size=1.0):
    """
    Génère des points sur une trajectoire avec un pas constant.

    :param trajectory: Liste de points (x, y) représentant la trajectoire.
    :param step_size: Distance constante entre deux points consécutifs.
    :return: Liste de nouveaux points (x, y) avec un pas constant.
    """
    # Extraire les coordonnées x et y
    x, y = zip(*trajectory)
    
    # Créer une interpolation paramétrique avec splines
    tck, u = splprep([x, y], s=0)  # 's=0' signifie que l'on suit exactement les points
    unew = np.linspace(0, 1, num=1000)  # Augmenter la résolution pour précision
    
    # Générer des points interpolés
    interpolated_points = np.array(splev(unew, tck))
    
    # Calculer les distances cumulées le long de la trajectoire
    dx = np.diff(interpolated_points[0])
    dy = np.diff(interpolated_points[1])
    distances = np.sqrt(dx**2 + dy**2)
    cumulative_distances = np.hstack(([0], np.cumsum(distances)))
    
    # Générer les nouveaux points avec un pas constant
    total_length = cumulative_distances[-1]
    new_distances = np.arange(0, total_length, step_size)
    new_points = np.array(splev(new_distances / total_length, tck)).T

    return new_points

def main():
    image_path = "trace.png"  # Chemin vers l'image Paint contenant le tracé
    try:
        trajectory = extract_trajectory_from_image(image_path)
        new_trajectory = generate_constant_step_points(trajectory, step_size=1.0)
        print("Trajectoire interpolé extraite :")
        print(new_trajectory)
        
        # Visualiser la trajectoire (facultatif)
        image = cv2.imread(image_path)
        for point in new_trajectory:
            # Convertir le point en tuple d'entiers
            center = tuple(int(coord) for coord in point)
            cv2.circle(image, center, 1, (0, 0, 255), -1)
        cv2.imshow("Trajectoire", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    main()