from flask import Flask, request, render_template
import fitz  # PyMuPDF
import re

app = Flask(__name__)

def extract_text_from_pdf():
    with fitz.open("cutoff2024.pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

def predict_colleges(text, percentile, category):
    results = []
    pattern = re.compile(rf'({category})\s+\d+\s+\((\d+\.\d+)\)', re.IGNORECASE)
    for match in pattern.finditer(text):
        cat, cut_percentile = match.groups()
        if float(percentile) >= float(cut_percentile):
            results.append(f"{cat} - Cutoff: {cut_percentile}%")
    return sorted(set(results)) if results else ["No matching colleges found."]

from flask import abort

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            percentile = float(request.form['percentile'])
            category = request.form['category'].strip().upper()
        except:
            return abort(400)  # If input is invalid or missing

        text = extract_text_from_pdf()
        colleges = predict_colleges(text, percentile, category)
        return render_template('result.html', colleges=colleges)
    return render_template('index.html')


if __name__ == '__main__':
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

