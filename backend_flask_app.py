from flask import Flask, request, jsonify
from flask_cors import CORS
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from PIL import Image


print("reportlab is working!")

app = Flask(__name__)
CORS(app)

os.makedirs("static", exist_ok=True)



@app.route("/generate_pdf", methods=["POST"])
def generate_pdf():
    try:
        link = request.form.get("link")
        image_file = request.files.get("image")

        if not link or not image_file:
            return jsonify({"error": "Missing link or image"}), 400

        # Save uploaded image to static folder
        image_path = os.path.join("static", image_file.filename)
        image_file.save(image_path)

        # Create a PDF with clickable overlay
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter

        pdf_filename = os.path.splitext(image_file.filename)[0] + ".pdf"
        pdf_path = os.path.join("static", pdf_filename)

        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        # Draw full-page image
        c.drawImage(image_path, 0, 0, width=width, height=height)

        # Add clickable overlay
        c.linkURL(link, (0, 0, width, height), relative=0)

        c.showPage()
        c.save()

        # Clean up
        os.remove(image_path)

        return jsonify({ "pdfUrl": f"/static/{pdf_filename}" })

    except Exception as e:
        print("❌ ERROR during PDF generation:", e)
        return jsonify({ "error": "Server error during PDF creation." }), 500



if __name__ == "__main__":
    app.run(debug=True)
