from flask import Flask, request, jsonify
from flask_cors import CORS
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from PIL import Image
import io
import uuid


# print("reportlab is working!")



app = Flask(__name__)
CORS(app)

os.makedirs("static", exist_ok=True)

@app.route("/generate_pdf", methods=["POST"])
def generate_pdf():
    try:
        link = request.form.get("link")
        file = request.files.get("image")

        if not link or not file:
            return jsonify({"error": "Missing link or image"}), 400

        # Open image
        img = Image.open(file.stream)
        img_width, img_height = img.size

        # Create PDF
        pdf_filename = f"{uuid.uuid4().hex}.pdf"
        pdf_path = os.path.join("static", pdf_filename)

        c = canvas.Canvas(pdf_path, pagesize=(img_width, img_height))
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        c.drawImage(img_bytes, 0, 0, width=img_width, height=img_height)
        c.linkURL(link, (0, 0, img_width, img_height), relative=0)
        c.showPage()
        c.save()

        return jsonify({ "pdfUrl": f"/static/{pdf_filename}" })

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
