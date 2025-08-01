# quicklinkbackend/app.py

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from PIL import Image
import io
import uuid

app = Flask(__name__)
CORS(app)

# Ensure static folder exists
os.makedirs("static", exist_ok=True)

@app.route("/generate_pdf", methods=["POST"])
def generate_pdf():
    link = request.form.get("link")
    file = request.files.get("image")

    if not link or not file:
        return jsonify({"error": "Missing link or image"}), 400

    # Open image using PIL
    img = Image.open(file.stream)
    img_width, img_height = img.size

    # Convert pixel size to PDF point size
    pdf_filename = f"{uuid.uuid4().hex}.pdf"
    pdf_path = os.path.join("static", pdf_filename)

    # Create PDF canvas with image size
    c = canvas.Canvas(pdf_path, pagesize=(img_width, img_height))

    # Draw the image at (0,0)
    img_byte = io.BytesIO()
    img.save(img_byte, format='PNG')
    img_byte.seek(0)
    c.drawImage(img_byte, 0, 0, width=img_width, height=img_height)

    # Add invisible clickable link overlay
    c.linkURL(link, (0, 0, img_width, img_height), relative=0)

    c.showPage()
    c.save()

    return jsonify({
        "pdfUrl": f"/static/{pdf_filename}"
    })

if __name__ == "__main__":
    app.run(debug=True)
