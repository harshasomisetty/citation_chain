import pandas as pd
import json
import os
from collections import defaultdict

blockspace_path = "blockspace.json"
#read csv file

df = pd.read_csv('output_1.csv')
df["Conference"] = df["Conference"].str.strip()

metrics = ["Citations", "References", "Authors", "Pages", "CitationVelocity", "#AuthorsofAffiliations", "#DocumentsofAffiliation", "#DocsbyAuthors", "hIndexAuthors", "PlumX", "PageRank"]

block_data = None

def get_confs_names(): # Returns list of conferences added.
    return [conf[0] for conf in block_data[1]]


def get_conf(conf_name): # Returns conf block of data (includes years, metrics).
    for conf in block_data[1]:
        if conf_name == conf[0]:
            return conf
    return []

def get_conf_and_year(conf_name, year_name): # Returns year block from a conf.
    conf = get_conf(conf_name)
    for year in conf[2]:
        if year_name == year[0]:
            return year
    return None

def get_conf_year_list(conf_name): # Returns list of years in a conference.
    if get_conf(conf_name):
        return [year[0] for year in get_conf(conf_name)[2]]
    else:
        return []

def get_conf_papers(conf_name): # Get all papers in a conference.
    conf = get_conf(conf_name)
    papers = []
    for year in conf[2]:
        papers += year[2]

    return papers

def get_conf_year_papers(conf_name, year_check): # Get all papers in a year of a conf.
    conf = get_conf(conf_name)
    for year in conf[2]:
        if year[0]==year_check:
            return year[2]

    return []



def papers_in_conf_year(conf_check, year_check):
    paper_dois = []
    if year_check in get_conf_year_list(conf_check):
        for year in get_conf(conf_check)[2]:
            if year_check == year[0]:
                paper_dois = year[2]



def insert_paper(paper): # 
    global block_data
    
    def insert_new_year(paper, conf):
        new_year = [paper[1], [m[:3] for m in metrics], [paper[0]]]
        conf[2].append(new_year)
        
    conf_modify = []

    inserted = False
    for ind, conf in enumerate(block_data[1]):
        if paper[2] == conf[0]:
            conf_modify=block_data[1].pop(ind)

    if not conf_modify:
        conf_modify = [paper[2], [m[:3] for m in metrics], []]
        insert_new_year(paper, conf_modify)
    else:
        for year in conf_modify[2]:
            if year[0] == paper[1]:
                year[2].append(paper[0])
                inserted = True
                
        if not inserted:
            insert_new_year(paper, conf_modify)
        
    block_data[1].append(conf_modify)
    return



def clear_block_data():
    if os.path.exists(blockspace_path):
        os.remove(blockspace_path)
        
    with open(blockspace_path, 'w') as f:
        pass

def init_data():
    global block_data

    clear_block_data()
    
    block_data = [[], []]
    for ind, metric in enumerate(metrics):
        block_data[0].insert(ind, "")

    if os.stat(blockspace_path).st_size == 0:
        print('File is empty, initing genesis block')
        json_data = {-1: block_data}
        with open(blockspace_path, "w+") as f:
            json.dump(json_data, f)

def load_block_data():
    with open(blockspace_path, 'r+') as f:
        return json.load(f)


def read_block(new_block_index=None):

    global block_data

    data = load_block_data()

    if not new_block_index:
        new_block_index = list(data.keys())[-1]

    block_data = data[new_block_index]
    

def save_block():

    global block_data
    data = load_block_data()

    new_block_index = str(int(list(data.keys())[-1])+1)

    data[new_block_index] = block_data

    with open(blockspace_path, 'w+') as f:
        json.dump(data, f)
    

def create_block(batch):
    new_inserts = defaultdict(lambda: [])
    result = [[*f] for f in zip(batch["PaperId"], batch["Year"], batch["Conference"])]

    read_block()
    for i in result:
        insert_paper(i)
        if i[1] not in new_inserts[i[2]]:
            new_inserts[i[2]].append(i[1])

    
    return new_inserts

        
def block_routine(batch):

    def get_top_paper(papers, metric):
        found_batch = df[df["PaperId"].isin(papers)]
        return found_batch.sort_values(by=[metric], ascending=False)[["Paper", metric]].head(1).values.tolist()[0]

    def set_block_metrics(metric_ptr, papers):
        for ind, metric in enumerate(metrics):
            top_paper = get_top_paper(papers, metric)
            metric_ptr[ind] = top_paper[0]
    new_inserts = create_block(batch)


    print("new inserts", new_inserts, "\n")

    new_all_papers = []
    for conf in new_inserts.keys():
        conf_block = get_conf(conf)
        new_conf_papers = []
        for year in new_inserts[conf]:

            new_year_papers = get_conf_year_papers(conf, year)
            new_conf_papers += new_year_papers
            
            year_block = get_conf_and_year(conf, year)

            set_block_metrics(year_block[1], new_year_papers)

        set_block_metrics(conf_block[1], new_conf_papers)
                
        new_all_papers += new_conf_papers

    set_block_metrics(block_data[0], new_all_papers)
    save_block()
    print(block_data, "\n")

if __name__ == "__main__":
    init_data()
    # clear_block_data()
    block_length = 3
    for i in range(5,7):
        batch = df[i*block_length: i*block_length+block_length]
        print(batch[["Paper"]])
        block_routine(batch)
        
