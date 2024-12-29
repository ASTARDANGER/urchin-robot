import matplotlib.pyplot as plt
import numpy as np
from skimage import io, color
from scipy.interpolate import splprep, splev
import matplotlib.colors as mplcolors

## to plot with a gradient of color
def colorFader(c1="green",c2="red",mix=0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    c1=np.array(mplcolors.to_rgb(c1))
    c2=np.array(mplcolors.to_rgb(c2))
    return mplcolors.to_hex((1-mix)*c1 + mix*c2)

def find_path_with_all_black_pixels(image_path, num_points):
    # Load the image
    image = io.imread(image_path)

    # Check for RGBA images and convert to RGB if needed
    if image.shape[-1] == 4:  # RGBA
        image = image[:, :, :3]

    # Detect start (green) and end (red) points
    start_point = np.argwhere((image == [0, 255, 0]).all(axis=2))
    end_point = np.argwhere((image == [255, 0, 0]).all(axis=2))

    if len(start_point) == 0 or len(end_point) == 0:
        raise ValueError("Start or end point not found in the image.")

    start_point = start_point[0]
    end_point = end_point[0]

    # Convert image to grayscale and detect black pixels
    image_gray = color.rgb2gray(image)
    black_pixels = np.argwhere(image_gray < 0.1)

    if len(black_pixels) == 0:
        raise ValueError("No black pixels detected in the image.")

    # Reorder black pixels to construct a continuous path
    path = [start_point]
    remaining_pixels = set(map(tuple, black_pixels))
    remaining_pixels.discard(tuple(start_point))

    current_point = start_point
    while remaining_pixels:
        nearest_pixel = min(remaining_pixels, key=lambda p: np.linalg.norm(np.array(p) - current_point))
        path.append(nearest_pixel)
        remaining_pixels.remove(nearest_pixel)
        current_point = nearest_pixel

    path = np.array(path)

    # Smooth the path with spline interpolation
    tck, u = splprep([path[:, 1], path[:, 0]], s=len(path[:, 1]))
    u_new = np.linspace(0, 1, num_points)
    x_new, y_new = splev(u_new, tck)

    # Visualization
    plt.figure(figsize=(10, 10))
    plt.imshow(image, origin='upper')
    plt.plot(path[:, 1], path[:, 0], 'blue', label="Detected Path")
    for i in range(len(x_new)):
        plt.scatter(x_new[i], y_new[i], color=colorFader("darkblue", "lightblue", i/len(x_new)), s=20)
    plt.scatter(start_point[1], start_point[0], color='green', label="Start", s=50)
    plt.scatter(end_point[1], end_point[0], color='red', label="End", s=50)
    plt.legend()
    plt.axis('off')
    plt.title("Path Following All Black Pixels")
    plt.show()

    # Return waypoints
    return np.array(list(zip(x_new, y_new)))

# Example usage
image_path = "path.png"  # Replace with your image path
num_points = 500
waypoints = find_path_with_all_black_pixels(image_path, num_points)