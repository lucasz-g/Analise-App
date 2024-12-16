from flask import Flask, request, render_template, send_file
import pandas as pd
from pandas_profiling import ProfileReport
import os

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
REPORT_FOLDER = './reports'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('./index.html') # Interface frontend

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_format = request.form['format']  # csv, excel, json

    # Salvar o arquivo enviado
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Ler o arquivo para um DataFrame
    if file_format == 'csv':
        df = pd.read_csv(file_path)
    elif file_format == 'excel':
        df = pd.read_excel(file_path)
    elif file_format == 'json':
        df = pd.read_json(file_path)
    else:
        return "Formato não suportado", 400

    # Gerar o relatório de Pandas Profiling
    profile = ProfileReport(df, title="Análise Exploratória", explorative=True)
    report_path = os.path.join(REPORT_FOLDER, 'report.html')
    profile.to_file(report_path)

    return send_file(report_path, as_attachment=True)  # Download do relatório

if __name__ == '__main__':
    app.run(debug=True)