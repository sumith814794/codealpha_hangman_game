import os
from flask import Flask, render_template, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

template_dir = os.path.join(BASE_DIR, "templates")
static_dir = os.path.join(BASE_DIR, "static")

app = Flask(
    __name__,
    template_folder=template_dir,
    static_folder=static_dir
)

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(static_dir, filename)

@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def home():
    return render_template("index.html")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" [*] CodeAlpha Hangman Web UI is running!")
    print(" [*] Open in your browser: http://127.0.0.1:5002")
    print("=" * 60 + "\n")
    app.run(debug=True, port=5002)
