from PIL import Image
from sklearn.cluster import KMeans
import numpy as np

def is_skin(r, g, b):
    return (
        r > 95 and g > 40 and b > 20 and
        max(r, g, b) - min(r, g, b) > 15 and
        abs(r - g) > 15 and r > g and r > b
    )

def detect_skin_tones(image_path, clusters=3):
    image = Image.open(image_path).convert('RGB')
    image = image.resize((150, 150))

    # Crop to center region
    w, h = image.size
    left = int(w * 0.25)
    top = int(h * 0.25)
    right = int(w * 0.75)
    bottom = int(h * 0.75)
    image = image.crop((left, top, right, bottom))

    pixels = np.array(image).reshape((-1, 3))
    skin_pixels = np.array([p for p in pixels if is_skin(*p)])

    if len(skin_pixels) < clusters:
        skin_pixels = pixels

    kmeans = KMeans(n_clusters=clusters, n_init=10)
    labels = kmeans.fit_predict(skin_pixels)
    dominant_colors = kmeans.cluster_centers_.astype(int)

    # Count most frequent cluster
    dominant_index = np.bincount(labels).argmax()
    dominant_color = dominant_colors[dominant_index]

    # Convert to hex
    hex_color = '#%02x%02x%02x' % tuple(dominant_color)
    return [hex_color]
