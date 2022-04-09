import os
from flask import Flask, render_template



# List of metadata files to ignore.
ignore = [".DS_Store", ]

# Data directory path of stored documents
dir = "data1/"
app = Flask(__name__, static_folder=dir)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/index')
def index():
    name = 'Rosalia'
    return render_template('index.html', title='Welcome', username=name)

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
            return render_template('content.html', title='Content', content = content)
        else:

            subdirs = []
            subfiles = []
            for file in os.listdir(path):
                if file not in ignore:
                    d = os.path.join(path, file)
                    if os.path.isdir(d):
                        subdirs.append(file)
                    else:
                        subfiles.append(file)

            return render_template('directory.html', title='Content', subdirs = sorted(subdirs), subfiles = sorted(subfiles), path = "/dir/"+path_user)
            
        
    else:
        return "Not a existing file"


if __name__ == '__main__':
  app.run(debug =True)


