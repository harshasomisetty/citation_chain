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

# conf: [conf_name, metrics, [years]]
# year: [year_name, metrics, [papers]]

def get_confs_names():
    return [conf[0] for conf in block_data[1]]


def get_conf(conf_name):
    for conf in block_data[1]:
        if conf_name == conf[0]:
            return conf
    return []

def get_conf_and_year(conf_name, year_name):
    conf = get_conf(conf_name)
    for year in conf[2]:
        if year_name == year[0]:
            return year
    return None

def get_conf_year_list(conf_name):
    if get_conf(conf_name):
        return [year[0] for year in get_conf(conf_name)[2]]
    else:
        return []


def check_year_in_conf(conf_name, year_to_check):
    return year_to_check in get_conf_year_list(conf_name)

def get_conf_papers(conf_name):
    conf = get_conf(conf_name)
    papers = []
    for year in conf[2]:
        papers += year[2]

    return papers

def get_conf_year_papers(conf_name, year_check):
    conf = get_conf(conf_name)
    for year in conf[2]:
        if year[0]==year_check:
            return year[2]

    return []


def clear_block_data():
    if os.path.exists(blockspace_path):
        os.remove(blockspace_path)
        
    with open(blockspace_path, 'w') as f:
        pass
    
def read_block():
    return



def insert_paper(paper):
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


def create_block(batch):
    new_inserts = defaultdict(lambda: [])
    result = [[*f] for f in zip(batch["PaperId"], batch["Year"], batch["Conference"])]

    for i in result:
        print(i)
        insert_paper(i)
        if i[1] not in new_inserts[i[2]]:
            new_inserts[i[2]].append(i[1])

    return new_inserts


def papers_in_conf_year(conf_check, year_check):
    paper_dois = []
    if check_year_in_conf(conf_check, year_check):
        for year in get_conf(conf_check)[2]:
            if year_check == year[0]:
                paper_dois = year[2]
    # print("DPOIS", paper_dois)
    
def init_data():
    global block_data
    block_data = [[], []]
    block_data_indexes = []
    for ind, metric in enumerate(metrics):
        block_data[0].insert(ind, "")
    # print("inited", block_data)
        
def block_routine(batch):
    
    new_inserts = create_block(batch)

    # print("\n\nfinal creation")
    print("new inserts", new_inserts, "\n")
    # print("conf year papers", get_conf_year_papers("SER&IP", 2021), "\n*****\n")


    new_all_papers = []
    for conf in new_inserts.keys():
        conf_block = get_conf(conf)
        new_conf_papers = []
        for year in new_inserts[conf]:

            new_year_papers = get_conf_year_papers(conf, year)
            new_conf_papers += new_year_papers
            
            year_block = get_conf_and_year(conf, year)

                        
            found_batch = df[df["PaperId"].isin(new_year_papers)]
            for ind, metric in enumerate(metrics):
                top_paper = found_batch.sort_values(by=[metric], ascending=False)[["Paper", metric]].head(1).values.tolist()[0]
                # print(ind, )
                year_block[1][ind] = top_paper[0]

        found_batch = df[df["PaperId"].isin(new_conf_papers)]
        for ind, metric in enumerate(metrics):
            top_paper = found_batch.sort_values(by=[metric], ascending=False)[["Paper", metric]].head(1).values.tolist()[0]
            conf_block[1][ind] = top_paper[0]
                
        new_all_papers += new_conf_papers
        
    found_batch = df[df["PaperId"].isin(new_all_papers)]
    for ind, metric in enumerate(metrics):
        top_paper = found_batch.sort_values(by=[metric], ascending=False)[["Paper", metric]].head(1).values.tolist()[0]
        block_data[0][ind] = top_paper[0]
    

    print("new_papgers", new_all_papers, "\n\n")

    

    

    print(block_data, "\n")

if __name__ == "__main__":
    init_data()
    # clear_block_data()
    for i in range(1):
        batch = df[i+10: i+13]
        block_routine(batch)
        
        
    


    # sort then rewrite the metrics for folder, conf, etc
