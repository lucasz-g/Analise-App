from flask import Flask, request, render_template, send_file, redirect, url_for
import pandas as pd
from ydata_profiling import ProfileReport
import os

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
REPORT_FOLDER = './reports'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('./index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        file_format = request.form['format']

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        if file_format == 'csv':
            df = pd.read_csv(file_path)
        elif file_format == 'excel':
            df = pd.read_excel(file_path)
        elif file_format == 'json':
            df = pd.read_json(file_path)
        else:
            return "Formato não suportado", 400

        profile = ProfileReport(df, title="Análise Exploratória", explorative=True)
        report_path = os.path.join(REPORT_FOLDER, 'report.html')
        profile.to_file(report_path)

        return redirect(url_for('view_report'))

    except Exception as e:
        return f"Ocorreu um erro: {str(e)}", 500

@app.route('/view_report')
def view_report():
    report_path = os.path.join(REPORT_FOLDER, 'report.html')
    # Enviar o arquivo diretamente como uma resposta HTTP para ser exibido em uma nova guia
    return send_file(report_path)

if __name__ == '__main__':
    app.run(debug=True)