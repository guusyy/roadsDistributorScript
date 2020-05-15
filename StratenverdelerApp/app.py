import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_weasyprint import HTML, render_pdf

from logic.myCSV import MyCSV
from logic.stratenVerdeler import StratenVerdeler

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(THIS_FOLDER, 'uploads/')
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/test.db' 
db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "overzicht_personen.csv"))
            uploadedCSV = MyCSV(os.path.join(THIS_FOLDER, 'uploads/overzicht_personen.csv'))    
            csvData = uploadedCSV.read()

            return render_template('succes.html', data=csvData)
        else:
            return render_template('index.html', errorSignal="wrongFormat")
    return render_template('index.html')

#runs the calculation
@app.route('/runCalculation', methods=['POST', 'GET'])
def runCalculation():
    firstNameClm = int(request.form.get("voornaamClm"))
    middleNameClm = int(request.form.get("tussennaamClm"))
    lastNameClm = int(request.form.get("achternaamClm"))
    birthDateClm = int(request.form.get("geboortedatumClm"))
    groupClm = int(request.form.get("groepClm"))
    streetClm = int(request.form.get("straatClm"))
    streetNumbrClm = int(request.form.get("huisnummerClm"))
    postalCodeClm = int(request.form.get("postcodeClm"))
    townClm = int(request.form.get("dorpClm"))
    filePath = os.path.join(THIS_FOLDER, 'uploads/overzicht_personen.csv')

    stratenVerdeler = StratenVerdeler(filePath, firstNameClm, middleNameClm, lastNameClm, birthDateClm, groupClm, streetClm, streetNumbrClm, postalCodeClm, townClm)
    finalData = stratenVerdeler.verdeelStratenOverKinderen("Gennep")

    return render_template('succesConverted.html', data=finalData)

@app.route('/formulierenPDF.pdf')
def hello_pdf(data):
    # Make a PDF straight from HTML in a string.
    html = render_template('pdf/formulierenPDF.html', data=data)
    return render_pdf(HTML(string=html))

@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template('index.html', errorSignal="fileTooLarge"), 413

if __name__ == "__main__":
    app.run(debug=True)