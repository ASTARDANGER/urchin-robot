import matplotlib.pyplot as plt
import numpy as np
from skimage import io, color, morphology
from skimage.graph import route_through_array

def plot_trajectory_with_points(image_path, num_points):
    # Charger l'image
    image = io.imread(image_path)

    # Vérifier si l'image a une quatrième dimension (canal alpha)
    if image.shape[-1] == 4:  # RGBA
        image = image[:, :, :3]  # Garder uniquement les trois canaux RGB

    # Identifier les pixels spécifiques
    start_point = np.argwhere((image == [0, 255, 0]).all(axis=2))  # Vert (départ)
    end_point = np.argwhere((image == [255, 0, 0]).all(axis=2))    # Rouge (arrivée)

    if len(start_point) == 0 or len(end_point) == 0:
        raise ValueError("Points de départ ou d'arrivée introuvables dans l'image")

    start_point = start_point[0]  # Supposons un seul pixel vert
    end_point = end_point[0]      # Supposons un seul pixel rouge

    print(f"Start point: {start_point}, End point: {end_point}")

    # Identifier les pixels de la trajectoire (noirs)
    image_gray = color.rgb2gray(image) if image.ndim == 3 else image
    path_mask = image_gray < 0.1  # Seuil pour les pixels noirs

    if not np.any(path_mask):
        raise ValueError("Aucun pixel noir trouvé pour la trajectoire")

    # Appliquer une dilatation pour connecter les pixels isolés
    path_mask = morphology.dilation(path_mask, morphology.square(3))

    # Créer une matrice de coût (inverse des valeurs du masque)
    cost_array = np.where(path_mask, 1, np.inf)

    # Trouver le chemin optimal entre le départ et l'arrivée
    try:
        indices, _ = route_through_array(cost_array, tuple(start_point), tuple(end_point), fully_connected=True)
    except ValueError as e:
        raise ValueError("Impossible de trouver un chemin entre les points") from e

    trajectory = np.array(indices)

    # Répartir N points équidistants le long de la trajectoire
    distances = np.cumsum(np.sqrt(np.sum(np.diff(trajectory, axis=0)**2, axis=1)))
    distances = np.insert(distances, 0, 0)
    target_distances = np.linspace(0, distances[-1], num_points)
    sampled_points = trajectory[np.searchsorted(distances, target_distances)]

    # Préparer l'affichage
    plt.figure(figsize=(10, 10))

    # Afficher l'image d'origine
    plt.imshow(image, origin='upper')

    # Tracer la trajectoire détectée
    plt.plot(trajectory[:, 1], trajectory[:, 0], color='blue', label="Trajectoire détectée")

    # Ajouter les points
    plt.scatter(start_point[1], start_point[0], color='green', label="Départ", s=100)
    plt.scatter(end_point[1], end_point[0], color='red', label="Arrivée", s=100)
    plt.scatter(sampled_points[:, 1], sampled_points[:, 0], color='yellow', label="Points échantillonnés", s=50)
    print(len(sampled_points))
    plt.legend()
    plt.axis('off')
    plt.title("Trajectoire détectée avec points de départ et d'arrivée")
    plt.show()

# Exemple d'utilisation
image_path = "path.png"
num_points = 1000
plot_trajectory_with_points(image_path, num_points)
