import os
from flask import Flask, render_template, request, redirect, send_file, url_for, send_from_directory
from s3connect import list_files, download_file, upload_file, apply_filter, delete_objects
from werkzeug.utils import secure_filename

UPLOAD_FOLDER="uploads/"
BUCKET="imageprobucket1"

app = Flask(__name__) 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/") 
def storage():
  contents = list_files(BUCKET)
  return render_template("index.html", contents=contents)

@app.route("/upload", methods=['POST'])
def upload():
  if request.method == "POST":
    # Get requested file
    f = request.files['file']
    # Secure that filename or smt
    filename = secure_filename(f.filename)
    # File into local storage
    f.save(os.path.join(app.config["UPLOAD_FOLDER"], f.filename))
    # Upload file to S3 Bucket
    upload_file(f"{f.filename}", BUCKET) 
    return redirect("/")

@app.route("/downloads/<filename>", methods=['GET'])
def download(filename):
  if request.method == 'GET':
    output = download_file(filename, BUCKET) 
    return send_file(output, as_attachment=True, attachment_filename=str(filename), mimetype='image/png')

@app.route("/applyfilter", methods=['POST'])
def applyfilter():
  print("Hello?")
  if request.method == "POST":
    filename = request.form.get("imagefile")
    filtertype = request.form.get("effect")  
    print(filename, filtertype)
    apply_filter(filename, filtertype, BUCKET)
    return redirect("/")

@app.route("/delete", methods=['POST']) 
def delete():
	if request.method == 'POST':
		objects = []
		for filename in request.form.getlist("imagefiles"):
			Object = {}
			Object["Key"] = filename 
			objects.append(Object)
		delete_dict = {}
		delete_dict["Objects"] = objects
		delete_objects(delete_dict, BUCKET)
	return redirect("/")

if __name__ == "__main__":
  app.run(debug=True)
