# tell you

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
	"Send a json response"

	response = json.dumps(data)
	return Response(response, code, mimetype="application/json")

def get_convert_command(filename, filetype):
	"Returns command to conv _filename_ to _filetype_"

	if filetype == 'docx':
	    cmd = ( "pandoc -f html %s -t docx -o %s" % (filename, filename+".docx") )
	elif filetype == 'pdf':
		cmd = ( "pandoc -f html %s  -o %s" % (filename, filename+".pdf") )
	return shlex.split(cmd)

# check valid extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/ping', methods=['GET'])
def ping():
	return Response('ping', 200)

@app.route('/conv', methods=['POST'])
def convert_file():

    if request.method == 'POST':
		try:
			filetype = request.form['filetype']
		except:
			return Response("Error in fetching filetype", 500)
		if filetype is None:
			return Response("Filetype is None", 500)

		file = request.files['file']
		if file and allowed_file(file.filename):
			fno, tempfilename = tempfile.mkstemp()
			tempfilename = tempfilename
			file.save(tempfilename)
			subprocess.call(get_convert_command(tempfilename, filetype), shell=False)
			with open(tempfilename+'.'+filetype, "r") as cr:
				content  = cr.read()
			return Response(content, 200)

    return Response(content, 403)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8800)
