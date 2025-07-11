from flask import Flask, request, render_template
import fitz  # PyMuPDF
import re

app = Flask(__name__)

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        percentile = float(request.form['percentile'])
        category = request.form['category'].strip().upper()
        file = request.files['pdf']
        text = extract_text_from_pdf(file)
        colleges = predict_colleges(text, percentile, category)
        return render_template('result.html', colleges=colleges)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
