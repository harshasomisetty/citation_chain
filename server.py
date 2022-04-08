import os
from flask import Flask, send_from_directory



# List of metadata files to ignore.
ignore = [".DS_Store"]

# Data directory path of stored documents
dir = "data1/"
app = Flask(__name__, static_folder=dir)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/dir')
@app.route('/dir/')
@app.route('/dir/<path:path_user>')
def access_path(path_user=""):
    if not path_user:
        path = dir
    else:
        path = dir+path_user
    if os.path.exists(path):
        if os.path.isfile(path):
            with open(path, "r") as f:
                content = f.read()
            return content
        else:

            subdirs = []
            subfiles = []
            for file in os.listdir(path):
                d = os.path.join(path, file)
                if os.path.isdir(d):
                    subdirs.append(file)
                else:
                    subfiles.append(file)

            return " ".join(subdirs)
            
        
    else:
        return "Not a existing file"


if __name__ == '__main__':
  app.run(debug =True)
