from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

def extract_data_from_excel():
    df = pd.read_excel("cutoff2024.xlsx")
    return df

def predict_colleges(df, percentile, category):
    category = category.strip().upper()

    if category not in df.columns:
        return []

    results = []
    for _, row in df.iterrows():
        try:
            cutoff = float(row[category])
            if percentile >= cutoff:
                results.append((row['College Name'], row['Branch'], category, cutoff))
        except:
            continue
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            percentile = float(request.form['percentile'])
            category = request.form['category']
        except:
            return "Invalid input", 400

        df = extract_data_from_excel()
        colleges = predict_colleges(df, percentile, category)
        return render_template('result.html', colleges=colleges)
    return render_template('index.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
