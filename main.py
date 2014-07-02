import os
from flask import Flask, request, redirect, Response
from werkzeug.utils import secure_filename
import subprocess
from flask import send_from_directory
import json
import tempfile
import subprocess
import shlex

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'py', 'html'])

app = Flask(__name__)
app.debug = True

def api_response(data, code=200):
    response = json.dumps(data)
    return Response(response, code, mimetype="application/json")

def convert_command(filename):
    return shlex.split( "pandoc -f html %s -t docx -o %s" % (filename, filename+".docx") )

# check valid extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/conv', methods=['POST'])
def upload_file():
	content = ''
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            fno, tempfilename = tempfile.mkstemp()
            file.save(tempfilename)
            print "Converting file: ", tempfilename
            subprocess.call(convert_command(tempfilename), shell=False)
            print "Conversion completed", tempfilename
            with open(tempfilename+".docx", "r") as cr:
                content  = cr.read()
            return Response(content, 200)
    return Response(content, 200)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8800)
