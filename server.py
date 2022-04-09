import os
import pandas
import json
from flask import Flask, render_template

# List of metadata files to ignore.
ignore = [".DS_Store", ]

# Data directory path of stored documents
dir = "data/"
app = Flask(__name__, static_folder=dir)

blockspace_path = "data/blockspace.json"
with open(blockspace_path, 'r') as f:
    data = json.load(f)

def find_paper(conf, metric):
    block_index = str(len(data) - 2)
    block = data[block_index]
    final_paper = ""
    print("finding", conf, metric)
    if metric in block.keys():
        for paper in block[metric]:
            if paper[2].strip() == conf:
                final_paper = paper[0]

        print("final: ", final_paper)
        return final_paper
    else:
        return "not metric"
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

    params = path_user.split("/")

    if os.path.exists(path):
        if os.path.isfile(path):
            metric = params[-1]
            conf = params[-2]
            with open(path, "r") as f:
                content = f.read()
            paper = find_paper(conf, metric)
            print("found", paper)
            return render_template('content.html', title='Content', content = content, conf = conf, metric = metric, paper = paper)
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


