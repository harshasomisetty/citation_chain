import pandas as pd
import json
import os
import shutil
from collections import defaultdict

directory_path = "data1/"
block_directory_path = "block_data/"
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


def load_block_data():
    with open(blockspace_path, 'r+') as f:
        return json.load(f)


def read_block():

    if os.stat(blockspace_path).st_size == 0:
        print('File is empty, initing genesis block')
        json_data = {-1: {metric: [] for metric in metrics}}
        with open(blockspace_path, "w+") as f:
            json.dump(json_data, f)

    data = load_block_data()

    new_block_index = list(data.keys())[-1]

    return data[new_block_index]


def insert_paper(prev_papers, new_paper):
    index = len(prev_papers)
    for i in range(len(prev_papers)):
        if prev_papers[i][1] < new_paper[1]:
            index = i
            break
    if index == len(prev_papers):
        prev_papers = prev_papers[:index]+[new_paper]
    else:
        prev_papers = prev_papers[:index]+[new_paper] + prev_papers[index:]
    return prev_papers


def create_block(batch):

    new_block = {}
    prev_block = read_block()

    for metric in metrics[:1]:
        cur_ranking = prev_block[metric]
        new_papers = batch[["Name", "Year", "Conference", metric]].sort_values(by=[metric], ascending=False)
        # print(new_papers)
        for paper in new_papers.values:
            cur_ranking = insert_paper(cur_ranking, list(paper))
        new_block[metric] = cur_ranking

    data = load_block_data()

    new_block_index = str(int(list(data.keys())[-1])+1)

    data[new_block_index] = new_block

    with open(blockspace_path, 'w+') as f:
         json.dump(data, f)

         
def init_directories_by_block():
        
    if os.path.exists(block_directory_path):
        shutil.rmtree(block_directory_path)

    
    if not os.path.exists(blockspace_path):
        with open(blockspace_path, "w+") as f:
            pass

    os.mkdir(block_directory_path)
     
    data = load_block_data()
    block_index = str(len(data) - 2)
    block = data[block_index]
    block_metrics = list(block.keys())

    block_data_dict = defaultdict(lambda: [])
    for metric in block_metrics:
        print(metric)

        with open(block_directory_path+metric, "w+") as f:
            print("wrote", block_directory_path+metric)
            f.write("*" + block[metric][0][0] + "* is the paper with highest " + metric + " across all confs")

        for paper in block[metric]:
            cur_name, cur_year, cur_conf = paper[0], str(paper[1]), paper[2]
            if not os.path.exists(block_directory_path+cur_conf):
                os.mkdir(block_directory_path+cur_conf)
                print("created dir", block_directory_path+cur_conf)
                
            if not os.path.exists(block_directory_path+cur_conf + "/" + metric):
                with open(block_directory_path+cur_conf + "/" + metric, "w+") as f:
                    f.write("*" + cur_name + "* is the paper with highest " + metric + " in conference " + cur_conf)
                    print("wrote file", block_directory_path+cur_conf + "/" + metric)

            if not os.path.exists(block_directory_path+cur_conf+"/"+cur_year):
                os.mkdir(block_directory_path+cur_conf+"/"+cur_year)
                print("created dir", block_directory_path+cur_conf+"/"+cur_year)
                
            if not os.path.exists(block_directory_path+cur_conf+"/"+cur_year+"/"+metric):
                with open(block_directory_path+cur_conf+"/"+cur_year+"/"+metric, "w+") as f:
                    f.write("*" + cur_name + "* is the paper with highest " + metric + " in conference " + cur_conf + " in year " + cur_year)
                    print("wrote file", block_directory_path+cur_conf+"/"+cur_year+"/"+metric)
                    
            block_data_dict[paper[2].strip()].append(paper[1])

    print("\n\n", block_data_dict)

    
def block_routine():
    if os.path.exists(blockspace_path):
        os.remove(blockspace_path)
        
    with open(blockspace_path, 'w') as f:
        pass
        
    for batch_ind in batch_indexes:
        batch = df[df["PaperID"].isin(batch_ind)]
        create_block(batch)


    data = load_block_data()

    print("block length", len(data))
    print(data["3"])

    
if __name__ == "__main__":
    block_routine()
    init_directories_by_block()
