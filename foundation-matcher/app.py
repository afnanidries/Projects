from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import numpy as np
import json
from utils.color_detection import detect_skin_tones
from utils.twitter_feed import get_brand_updates

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    twitter_updates = get_brand_updates()
    return render_template('index.html', twitter=twitter_updates)


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Use only the top-detected skin tone
        skin_tone = detect_skin_tones(filepath)[0]
        recommendations = match_foundation(skin_tone)
        twitter_updates = get_brand_updates()

        return render_template('results.html',
                               image_path=filepath,
                               skin_tone=skin_tone,
                               recommendations=recommendations,
                               twitter=twitter_updates)

def match_foundation(user_hex):
    def hex_to_rgb(h):
        return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))

    user_rgb = np.array(hex_to_rgb(user_hex))

    with open('data/foundations.json') as f:
        foundation_db = json.load(f)

    for product in foundation_db:
        product_rgb = np.array(hex_to_rgb(product['hex']))
        product['distance'] = np.linalg.norm(user_rgb - product_rgb)

    foundation_db.sort(key=lambda x: x['distance'])
    return foundation_db[:3]

if __name__ == '__main__':
    print("Launching Flask server...")
    app.run(debug=True)
