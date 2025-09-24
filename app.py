from flask import Flask
from routes.ocr import ocr_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(ocr_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
