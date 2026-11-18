import os
from flask import Flask, jsonify, Response, send_from_directory, make_response

BASE = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", "7860"))
app = Flask(__name__, static_folder=None)

@app.after_request
def security_headers(resp):
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if resp.mimetype == "text/html":
        resp.headers["Cache-Control"] = "no-cache"
    return resp

@app.get("/")
def home():
    return send_from_directory(BASE, "index.html")

@app.get("/health")
def health():
    return jsonify(status="ok", app="Pawan Studio AI"), 200

@app.get("/manifest.json")
def manifest():
    return send_from_directory(BASE, "manifest.json", mimetype="application/manifest+json")

@app.get("/sw.js")
def worker():
    response = make_response(send_from_directory(BASE, "sw.js", mimetype="application/javascript"))
    response.headers["Service-Worker-Allowed"] = "/"
    response.headers["Cache-Control"] = "no-cache"
    return response

@app.get("/ads.txt")
def ads_txt():
    # Set ADS_TXT_CONTENT to the exact seller record supplied by your ad provider.
    return Response(os.getenv("ADS_TXT_CONTENT", "# Add your verified ad-network record here.") + "\\n",
                    mimetype="text/plain")

@app.get("/<path:filename>")
def assets(filename):
    allowed = {"icon.svg", "icon-192.png", "icon-512.png", "robots.txt"}
    if filename in allowed:
        return send_from_directory(BASE, filename)
    return jsonify(error="Not found"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
