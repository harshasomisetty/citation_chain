from semanticscholar import SemanticScholar
from collections import defaultdict
from tqdm import tqdm


def calculate_page_rank(list_doi,references_list,main_paperid_list):
    dict=defaultdict(list)
    paperiddict={}
    sch = SemanticScholar(timeout=5)
    count=1
    #Store doi in dictionary and have its corresponding unique number
    for main_paperid in main_paperid_list:
        if main_paperid not in paperiddict:
            paperiddict[main_paperid]=count
            count+=1
    #Get references of all dois and store it in dict. Dict key is paper id and value is list of references
    for i in tqdm(range((list_doi))):
        references=references_list[i]
        main_paperid =main_paperid_list[i]
        for reference in references:
            paperid=reference['paperId']
            if paperid in paperiddict:
                dict[paperiddict[main_paperid]].append(paperiddict[paperid])
            else:
                paperiddict[paperid]=count
                dict[paperiddict[main_paperid]].append(count)
                count+=1
    outlinks_count={}
    paper_inlinks={}
    #Procedure 1 : To create outlinks and inlinks
    for paper in  dict:
        citations_list=dict[paper]
        outlinks_count[paper]=len(citations_list)
        for citation in citations_list:
            if citation in paper_inlinks:
                paper_inlinks[citation].append(paper)
            else:
                paper_inlinks[citation]=[]
                paper_inlinks[citation].append(paper)

    #Procedure 2: Modified Iterative PageRank Algorithm
    damping_factor=0.85
    page_rank={}
    updated_page_rank={}
    for paper in dict:
        page_rank[paper]=1
    while True:
        flag=True
        for paper_r in page_rank:
            current_score=page_rank[paper_r]
            if paper_r in paper_inlinks:
                inlinks_list=paper_inlinks[paper_r]
                new_score=0.0
                for inlink in inlinks_list:
                    if inlink in page_rank:
                        new_score+=page_rank[inlink]/outlinks_count[inlink]
                new_score=(1-damping_factor) + damping_factor*new_score
                if current_score!= new_score:
                    flag=False
                updated_page_rank[paper_r]=new_score
        if flag:
            break
        page_rank=updated_page_rank
        updated_page_rank={}

    maximum_score=max(page_rank.values())
    for paper_r in page_rank:
        page_rank[paper_r]/=maximum_score
    output_page_rank=[0]*list_doi
    for i in range(1,list_doi+1):
        if i in page_rank:
           output_page_rank[i-1]= page_rank[i]

    return output_page_rank










