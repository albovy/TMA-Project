from flask import Flask, request, abort, jsonify, send_from_directory
from flask_restful import Api, Resource, reqparse
from werkzeug.utils import secure_filename
import os
from data_model import DataModel

UPLOAD_FOLDER = "files"
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/ml", methods=["POST"])
def post_file():
    if 'file' not in request.files:
        return "", 500

    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return "No filename specified", 500
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        model = DataModel()
        result = model.classify(file_path)
        return "", 201


# api.add_resource(DataModel, '/ML')

if __name__ == '__main__':
    app.run()
