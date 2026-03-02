from flask import Flask, render_template
import subprocess
import threading
import os
import requests
from flask import Response

app = Flask(__name__)

def run_streamlit():
    subprocess.Popen([
        "python", "-m", "streamlit", "run", "app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0"
    ])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/streamlit")
def streamlit_proxy():
    resp = requests.get("http://127.0.0.1:8501")
    return Response(resp.content, content_type=resp.headers['Content-Type'])

if __name__ == "__main__":
    threading.Thread(target=run_streamlit).start()
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
