# backend/app.py

from flask import Flask, request, jsonify, send_file, redirect
from flask_cors import CORS
import os
import uuid
import json

app = Flask(__name__)
CORS(app)

# Store short links in memory or file (later use DB)
URL_STORE_PATH = "short_links.json"
if not os.path.exists(URL_STORE_PATH):
    with open(URL_STORE_PATH, 'w') as f:
        json.dump({}, f)


# Helper to save short link
def save_link(slug, long_url):
    with open(URL_STORE_PATH, 'r') as f:
        data = json.load(f)
    data[slug] = long_url
    with open(URL_STORE_PATH, 'w') as f:
        json.dump(data, f)


# Helper to get long URL
def get_long_url(slug):
    with open(URL_STORE_PATH, 'r') as f:
        data = json.load(f)
    return data.get(slug)


@app.route("/api/shorten", methods=["POST"])
def shorten():
    data = request.form
    long_url = data.get("longUrl")
    custom_name = data.get("customName", "")
    file = request.files.get("image")

    if not long_url:
        return jsonify({"error": "Missing long URL"}), 400

    slug = custom_name if custom_name else uuid.uuid4().hex[:6]

    # Save the link
    save_link(slug, long_url)

    # Save image if present
    if file:
        img_path = os.path.join("static", f"{slug}.jpg")
        file.save(img_path)
        # PDF generation will be added later

    return jsonify({"shortUrl": f"/r/{slug}", "slug": slug}), 200


@app.route("/r/<slug>")
def redirect_link(slug):
    long_url = get_long_url(slug)
    if long_url:
        return redirect(long_url)
    return "Invalid or expired link", 404


if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(debug=True)
