import pandas as pd
import json
import os
from collections import defaultdict

blockspace_path = "blockspace.json"

df = pd.read_csv('sample_dataset.csv')
df["Conference"] = df["Conference"].str.strip()

batch_indexes = [
    [1, 6, 11, 16, 21, 26],
    [2, 7, 12, 17, 22, 27],
    [3, 8, 13, 18, 23, 28],
    [4, 9, 14, 19, 24, 29],
    [5, 10, 15, 20, 25, 30]
]
metrics = ["Citations", "References", "Pages", "Words", "PaperScore"]

block_data = None

# conf: [conf_name, metrics, [years]]
# year: [year_name, metrics, [papers]]

def get_block_confs_names():
    return [conf[0] for conf in block_data[1]]


def get_block_conf(conf_name):
    for conf in block_data[1]:
        if conf_name == conf[0]:
            return conf
    return []

def get_conf_years(conf_name):
    return [year[0] for year in get_block_conf(conf_name)[2]]


def check_year_in_conf(conf_name, year_to_check):
    return year_to_check in get_conf_years(conf_name)


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
        new_year = [paper[1], metrics, [paper[0]]]
        conf[2].append(new_year)
        
    conf_modify = []

    # print("preinsert", block_data)
    for ind, conf in enumerate(block_data[1]):
        if paper[2] == conf[0]:
            conf_modify=block_data[1].pop(ind)

    if not conf_modify:
        conf_modify = [paper[2], metrics, []]
        insert_new_year(paper, conf_modify)
    else:
        # rewrite conf metrics
        # rewrite year metrics
        if conf_modify[2][0] == paper[1]: # existing year
            conf_modify[2][2].append(paper[0])
        else:
            new_year = [paper[1], metrics, [paper[0]]]
            insert_new_year(paper, conf_modify)
            # conf_modify[2].append(new_year)
        
    block_data[1].append(conf_modify)
    return


def create_block(batch):
    print("create block", block_data)
    print("Cols", batch.columns)
    new_inserts = defaultdict(lambda: [])
    result = [[*f] for f in zip(batch["Name"], batch["Year"], batch["Conference"])]
    for i in result:
        print(i)
        insert_paper(i)
        new_inserts[i[2]].append(i[1])


    print(new_inserts)
    print(check_year_in_conf("AAAI", 2014))
    print(block_data)


def init_data():
    global block_data
    block_data = [[], []]
    block_data_indexes = []
    for ind, metric in enumerate(metrics):
        block_data[0].insert(ind, "")
    print("inited", block_data)
        
def block_routine():
    init_data()


    for batch_ind in batch_indexes[:1]:
        batch = df[df["PaperID"].isin(batch_ind)]
        create_block(batch)
        


    # data = load_block_data()

    # print("block length", len(data))
    # print(data["3"])


if __name__ == "__main__":
    # clear_block_data()
    block_routine()

    # print(block_data)
    # init_data()
    # print(block_data)
