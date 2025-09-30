import os
import time
from flask import Blueprint, request, jsonify
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes
from utils.preprocess import preprocess_image

ocr_bp = Blueprint('ocr', __name__, url_prefix="/api")

OUTPUT_DIR = "texts"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@ocr_bp.route('/ocr', methods=['POST'])
def ocr_api():
    start_time = time.time()

    if 'image' not in request.files:
        return jsonify({"error": "campo 'image' faltando"}), 400
    if 'title' not in request.form:
        return jsonify({"error": "campo 'title' faltando"}), 400

    file = request.files['image']
    title = request.form['title'].strip()

    if file.filename == '':
        return jsonify({"error": "arquivo sem nome"}), 400
    if not title:
        return jsonify({"error": "título vazio"}), 400

    filename = file.filename.lower()
    texts = []

    try:
        if filename.endswith('.pdf'):
            pages = convert_from_bytes(file.read())
            for page in pages:
                processed = preprocess_image(page)
                pil_for_tesseract = Image.fromarray(processed)
                text = pytesseract.image_to_string(
                    pil_for_tesseract, config='', lang='por'
                )
                texts.append(text)
        else:
            processed = preprocess_image(file.stream)
            pil_for_tesseract = Image.fromarray(processed)
            text = pytesseract.image_to_string(
                pil_for_tesseract, config='', lang='por'
            )
            texts.append(text)

        final_text = "\n".join(texts)

        # Salvo normal
        file_path = os.path.join(OUTPUT_DIR, f"{title}.txt")

        # Append se o título já existir na pasta
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(final_text + "\n")

        end_time = time.time()
        execution_time = end_time - start_time

        return jsonify({
            "title": title,
            "text": final_text,
            "file_saved": file_path,
            "execution_time_sec": f"{round(execution_time, 3)} sec"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ocr_bp.route('/ocr/<title>', methods=['GET'])
def get_text_by_title(title):
    file_path = os.path.join(OUTPUT_DIR, f"{title}.txt")

    if not os.path.exists(file_path):
        return jsonify({"error": f"nenhum texto encontrado para título '{title}'"}), 404

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    return jsonify({
        "title": title,
        "text": content
    })

@ocr_bp.route('/ocr/', methods=['GET'])
def get_all_texts():
    texts = {}
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith('.txt'):
            title = filename[:-4] 
            file_path = os.path.join(OUTPUT_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                texts[title] = f.read()

    return jsonify(texts)