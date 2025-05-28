# 🎨 Foundation Matcher

**Foundation Matcher** is a lightweight, AI-powered web app that analyzes an uploaded image to detect your skin tone and recommend the closest matching foundation shades across top beauty brands. It uses computer vision and clustering to give real-time, personalized recommendations — all with user privacy in mind.

---

## 🌐 Live Demo

👉 [Try the app](https://foundation-matcher.onrender.com) 

---

## How It Works

1. Upload a selfie or facial image
2. The app crops to the central region of the face
3. K-means clustering is applied to detect your dominant skin tone
4. The app compares your tone to a curated product dataset
5. Top 3 closest matches are displayed with brand + shade info
6. A scrolling mock Twitter feed simulates live beauty brand updates

---

## Features

- Smart skin tone detection using pixel filtering and k-means
- Product match engine using color distance to real hex-coded shades
- Dynamic "brand tweet" feed using simulated data
- Fast and responsive UI using Bootstrap
- **Privacy-first**: Images are not stored or shared
- Designed for deployability and readability

---

## 🔧 Tech Stack

| Layer       | Tools Used                                      |
|-------------|--------------------------------------------------|
| Frontend    | HTML, CSS, Bootstrap, JavaScript (carousel)     |
| Backend     | Python Flask                                     |
| AI/ML Logic | scikit-learn (KMeans), Pillow, NumPy             |
| Mock Feed   | Python-generated data (no API dependency)        |
| Deployment  | Render                                           |

---

## 🔒 Privacy Disclaimer

> Uploaded images are processed temporarily in memory and never stored, logged, or shared. The app is designed for privacy-first use — ideal for users who want skin tone recommendations without giving up their data.

---

## API Considerations

Originally, we planned to integrate Twitter API for live brand updates. Due to recent pricing and access restrictions on Twitter's free tier, this feature was simulated with realistic mock tweets that cycle automatically. Future versions may support live Instagram or blog updates instead.

---

## ⚠️ Limitations & Future Work

- The tone matching is based on clustering and closest-hex logic — not full facial segmentation
- Expanding the product dataset to include more undertones and finishes would improve accuracy
- Optional user reviews, personalization, and login could be added with a database

---

## Lessons Learned

- I discovered that different types of images — especially those with varied lighting, backgrounds, or visible hair — significantly impacted skin tone detection. To address this, I refined my approach using center-cropping and skin-pixel filtering to get more accurate tone analysis.
- I initially experimented with multi-tone clustering, but it often returned visually inconsistent or misleading results. I decided to simplify the experience by focusing on the most dominant tone, which led to more accurate and trustworthy recommendations.
- I planned to integrate the Twitter API for live brand updates but pivoted due to access limitations. This challenge pushed me to simulate brand activity with a dynamic JavaScript feed that mimics real-time updates — a creative workaround that still enhanced the user experience.
- Building this app taught me how much preprocessing matters when working with image-based AI. Adapting to unexpected image types and edge cases helped me build a more resilient and user-friendly application.
- This project sparked ideas for future features like user reviews, real undertone detection, and deeper product personalization — which I plan to explore as I continue evolving this app.


---

## Local Development

```bash
# Clone the repo and go into the folder
git clone https://github.com/afnanidries/Projects.git
cd Projects/foundation-matcher

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

## 📫 Contact

- **Afnan Idries**
- 📍 Durham, NC  
- 📧 afnanidries@gmail.com  
- 🔗 [LinkedIn](https://linkedin.com/in/afnanidries)  
- 🔗 [GitHub](https://github.com/afnanidries)
