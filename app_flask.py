from flask import Flask, render_template
import subprocess
import threading
import os

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

if __name__ == "__main__":
    # Start Streamlit in background
    threading.Thread(target=run_streamlit).start()

    # Use Azure-assigned port
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
