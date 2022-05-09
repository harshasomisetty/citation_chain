import pandas as pd
import json
from flask import Flask, render_template


app = Flask(__name__)
blockspace_path = "blockspace.json"
with open(blockspace_path, 'r+') as f:
    data = json.load(f)

block_index = list(data.keys())[-1]
block_data = data[block_index]

df = pd.read_csv('output_1.csv')
metrics = list(df.columns[4:])
metrics.remove("Link")


def get_conf(conf_name): # Returns conf block of data (includes years, metrics).
    for conf in block_data[1]:
        if conf_name == conf[0]:
            return conf
    return []

def get_confs_names(): # Returns list of conferences added.
    return [conf[0] for conf in block_data[1]]

def get_conf_year_list(conf_name): # Returns list of years in a conference.
    if get_conf(conf_name):
        return [year[0] for year in get_conf(conf_name)[2]]
    else:
        return []

def get_conf_and_year(conf_name, year_name): # Returns year block from a conf.
    conf = get_conf(conf_name)
    for year in conf[2]:
        if year_name == year[0]:
            return year
    return None



@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/nav')
@app.route('/nav/')
def access_main():
    return render_template('main_page.html', metrics = metrics, confs = sorted(get_confs_names()))

@app.route('/nav/metric/<metric>')
def access_main_metric(metric):
    paper_data = block_data[0][metrics.index(metric)]
    return render_template('metric_page.html', paperDOI = paper_data[0], paper = paper_data[1], metric = metric)


@app.route('/nav/<conf>')
def access_conf(conf):
    if conf in get_confs_names():
        return render_template('conf_page.html', metrics = metrics, years = get_conf_year_list(conf), conf = conf)
    else:
        return "Not a conf"
    
@app.route('/nav/<conf>/metric/<metric>')
def access_conf_metric(conf,  metric):
    if conf in get_confs_names():
        conf_block = get_conf(conf)
        paper_data = conf_block[1][metrics.index(metric)]
        return render_template('metric_page.html', paperDOI = paper_data[0], paper = paper_data[1], metric = metric, conf = conf)
    else:
        return "metric doesn't exist in this conf"


@app.route('/nav/<conf>/<year>')
def access_year(conf, year):
    if conf in get_confs_names() and int(year) in get_conf_year_list(conf):
        return render_template('year_page.html', conf = conf, year = year, metrics = metrics)
    else:
        return "Not a year"

@app.route('/nav/<conf>/<year>/metric/<metric>')
def access_year_metric(conf, year, metric):
    if conf in get_confs_names() and int(year) in get_conf_year_list(conf):
        # conf_block = get_conf(conf)
        year_block = get_conf_and_year(conf, int(year))
        paper_data = year_block[1][metrics.index(metric)]
        return render_template('metric_page.html', paperDOI = paper_data[0], paper = paper_data[1], metric = metric, conf = conf, year = year)
    else:
        return "metric doesn't exist in this year"

if __name__ == '__main__':
  app.run(port=8080, host='0.0.0.0', debug = True)
