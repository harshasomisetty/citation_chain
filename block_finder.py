import pandas
import json
import os

blockspace_path = "data/blockspace.json"
df = pandas.read_csv('sample_dataset.csv')

batch_indexes = [
    [1, 6, 11, 16, 21, 26],
    [2, 7, 12, 17, 22, 27],
    [3, 8, 13, 18, 23, 28],
    [4, 9, 14, 19, 24, 29],
    [5, 10, 15, 20, 25, 30]
]
metrics = ["Year", "Citations", "References", "Pages", "Words", "PaperScore"]

def read_block():

    if os.stat(blockspace_path).st_size == 0:
        print('File is empty, initing genesis block')
        json_data = {-1: {metric: [] for metric in metrics}}
        with open(blockspace_path, "w+") as f:
            json.dump(json_data, f)

    with open(blockspace_path, 'r+') as f:
        data = json.load(f)

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

    for metric in metrics[1:2]:
        cur_ranking = prev_block[metric]
        new_papers = batch[["Name", metric]].sort_values(by=[metric], ascending=False)
        for paper in new_papers.values:
            cur_ranking = insert_paper(cur_ranking, list(paper))
        new_block[metric] = cur_ranking

    with open(blockspace_path, 'r') as f:
        data = json.load(f)

    new_block_index = str(int(list(data.keys())[-1])+1)

    data[new_block_index] = new_block

    with open(blockspace_path, 'w+') as f:
         json.dump(data, f)


def dfinterface():
    return
    # will inhereit same directory struct of conferences
    # inhereit same metrics
    # when person queries, will read latest block and that metric, display the top paper



def block_routine():
    if os.path.exists(blockspace_path):
        
        os.remove(blockspace_path)
        with open(blockspace_path, 'w') as f:
            pass
        print(os.listdir("."))
        
    for batch_ind in batch_indexes[:2]:
        batch = df[df["PaperID"].isin(batch_ind)]
        create_block(batch)


    with open(blockspace_path, 'r') as f:
        data = json.load(f)

    print("-1", data["-1"], "\n\n")
    print("0", data["0"], "\n\n")
    print("1", data["1"], "\n\n")


def init_directories():
    confs = list(set([v.strip() for v in df["Conference"].values]))

    for conf in confs:
        if not os.path.exists("data/"+conf):
            os.mkdir("data/"+conf)
        for metric in metrics:
            with open("data/"+conf+"/"+metric, 'w') as f:
                pass
    # print(confs)
    
if __name__ == "__main__":
    # init_directories()
    block_routine()
