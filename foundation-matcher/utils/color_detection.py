from PIL import Image
from sklearn.cluster import KMeans
import numpy as np

def detect_skin_tone(image_path, clusters=3):
    image = Image.open(image_path)
    image = image.resize((150, 150))  # Resize for faster processing
    image_np = np.array(image)

    # Flatten image pixels
    pixels = image_np.reshape((-1, 3))

    # Apply k-means clustering
    kmeans = KMeans(n_clusters=clusters, n_init=10)
    kmeans.fit(pixels)
    dominant = kmeans.cluster_centers_.astype(int)

    # Convert RGB values to hex
    hex_colors = ['#%02x%02x%02x' % tuple(color) for color in dominant]

    # Return most dominant tone (first in array)
    return hex_colors[0]
