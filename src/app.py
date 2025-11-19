from flask import Flask, request, send_file, render_template_string
import pandas as pd
from io import BytesIO

app = Flask(__name__)

# Health check
@app.route("/health")
def health():
    return {"status": "ok"}

# Web form for uploading CSV
@app.route("/", methods=["GET"])
def index():
    return render_template_string("""
    <!doctype html>
    <title>Upload CSV for Cleaning</title>
    <h1>Upload CSV for Cleaning</h1>
    <form action="/clean" method="post" enctype="multipart/form-data">
      <input type="file" name="file" required>
      <input type="submit" value="Clean">
    </form>
    """)

# Cleaning function: fill NaN with 0
def clean_dataframe(df):
    df = df.copy()
    df = df.fillna(0)
    return df

# Cleaning endpoint
@app.route("/clean", methods=["POST"])
def clean():
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        return "No file uploaded", 400

    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Clean data
    cleaned_df = clean_dataframe(df)

    # Prepare file for download
    buffer = BytesIO()
    cleaned_df.to_csv(buffer, index=False)
    buffer.seek(0)

    # Get original filename
    original_name = uploaded_file.filename
    cleaned_name = f"cleaned_{original_name}"

    # Send as downloadable file
    return send_file(buffer,
                     as_attachment=True,
                     download_name=cleaned_name,
                     mimetype="text/csv")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)
