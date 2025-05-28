from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

from utils.color_detection import detect_skin_tone
from utils.twitter_feed import get_brand_updates

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

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

        skin_tone = detect_skin_tone(filepath)
        recommendations = match_foundation(skin_tone)
        twitter_updates = get_brand_updates()

        return render_template('results.html',
                               image_path=filepath,
                               skin_tone=skin_tone,
                               recommendations=recommendations,
                               twitter=twitter_updates)

def match_foundation(skin_tone):
    # Simulate product matching
    return [
        {'brand': 'Fenty Beauty', 'product': 'Pro Filt\'r Soft Matte', 'shade': '290'},
        {'brand': 'NARS', 'product': 'Natural Radiant Longwear', 'shade': 'Punjab'},
        {'brand': 'Maybelline', 'product': 'Fit Me Matte + Poreless', 'shade': '228 Soft Tan'}
    ]

if __name__ == '__main__':
    app.run(debug=True)
