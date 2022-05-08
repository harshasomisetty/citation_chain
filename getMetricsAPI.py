import pandas as pd
from pybliometrics.scopus import AbstractRetrieval
from semanticscholar import SemanticScholar
from pybliometrics.scopus import AffiliationRetrieval
from pybliometrics.scopus import AuthorRetrieval
import csv,time,requests
from pybliometrics.scopus import PlumXMetrics
from pagerank import calculate_page_rank
from tqdm import tqdm

class calc:
    def __init__(self):
            self.references=[]
            self.main_paperid=[]
            self.final_doi_count=0

    def get_metrics(self,doi):
        try:
            metrics_scopus= AbstractRetrieval(doi, view='FULL')
        except:
            return
        time.sleep(1)
        
        sch = SemanticScholar(timeout=10)
        metrics_semanticscholar = sch.paper(doi)
        paper_title=metrics_scopus.title
        conf=["FSE","AAAI","ACL","CHI","CIKM","CVPR","FOCS","ICCV","ICML","ICSE","IJCAI","INFOCOM","KDD","MOBICOM","NeurIPS","NSDI","OSDI","PLDI","PODS","S&P","SIGCOMM","SIGIR","SIGMETRICS","SIGMOD","SODA","SOSP","STOC","UIST","VLDB","WWW"]
        # connferencename= next(substring for substring in conf if substring in metrics_scopus.confname)
        connference_name="Null"
        if 'venue' in metrics_semanticscholar.keys():
            if len(metrics_semanticscholar['venue'].split(" "))==1:
                connference_name=metrics_semanticscholar['venue'].split(" ")[0]
            for c in conf:
                if c in metrics_semanticscholar['venue'].split(" "):
                    connference_name=c
                    break
            if connference_name=="Null":
                s=metrics_semanticscholar['venue']
                if "(" in s and ")" in s:
                    connference_name=s[s.find("(")+1:s.find(")")]
                else:
                    connference_name=s
        year=int(metrics_scopus.coverDate.split("-")[0])
        if 'citations' in metrics_semanticscholar.keys():
            number_of_citations= len(metrics_semanticscholar['citations'])
        else:
            number_of_citations=0
        number_of_references=metrics_scopus.refcount
        number_of_authors=len(metrics_scopus.authors)
        if metrics_scopus.endingPage and metrics_scopus.startingPage and metrics_scopus.endingPage.isdecimal() and metrics_scopus.startingPage.isdecimal():
            number_of_pages= int(metrics_scopus.endingPage)-int(metrics_scopus.startingPage)
        else:
            number_of_pages=0
        if 'references' in metrics_semanticscholar.keys():
            self.references.append(metrics_semanticscholar['references'])
        else:
            self.references.append([])
        if 'paperId' in metrics_semanticscholar.keys():
            self.main_paperid.append(metrics_semanticscholar['paperId'])
        else:
            self.main_paperid.append('')
        if 'citationVelocity' in metrics_semanticscholar.keys():
            citationVelocity=metrics_semanticscholar['citationVelocity']
        else:
            citationVelocity=0
        
        #Affiliation details
        aff_info= metrics_scopus.affiliation
        numberOfAuthorsAffiliation=0
        numberOfDocumentsAffiliation=0
        if aff_info != None:
            for a in aff_info:
                aff_id=a[0]
                try:
                    aff = AffiliationRetrieval(aff_id)
                except:
                    continue
                numberOfAuthorsAffiliation+=aff.author_count
                numberOfDocumentsAffiliation+=aff.document_count
        #Authors details
        authors_info=metrics_scopus.authors
        numberOfDocsByAuthors=0
        hIndexOfAuthors=0
        if authors_info != None:
            for auth in authors_info:
                auth_id=auth[0]
                try:
                    author = AuthorRetrieval(auth_id)
                except:
                    continue
                numberOfDocsByAuthors+=author.document_count
                hIndexOfAuthors+=author.h_index
        
        plumXmetrics=0
        try:
            plum = PlumXMetrics(doi, id_type='doi')
        except:
            plum = None
        if plum!=None:
            plummetrics=plum.category_totals
            if plummetrics != None:
                for cat in plummetrics:
                    plumXmetrics+=cat[1]
        link=metrics_scopus.scopus_link
        list=[doi,paper_title,year,connference_name,number_of_citations,number_of_references,number_of_authors,number_of_pages,citationVelocity,numberOfAuthorsAffiliation,numberOfDocumentsAffiliation,numberOfDocsByAuthors,hIndexOfAuthors,plumXmetrics,link]
        # print("paper_title",paper_title)
        # print("connference_name",connference_name)
        # print("number_of_citations",number_of_citations)
        # print("number_of_references",number_of_references)
        # print("number_of_authors",number_of_authors)
        # print("number_of_pages",number_of_pages)
        # print("citationslist",citationslist)
        # print("citationVelocity",citationVelocity)
        # print("numberOfAuthorsAffiliation",numberOfAuthorsAffiliation)
        # print("numberOfDocumentsAffiliation",numberOfDocumentsAffiliation)
        # print("numberOfDocsByAuthors",numberOfDocsByAuthors)
        # print("hIndexOfAuthors",hIndexOfAuthors)
        # print("numberOfDocsCitedByOtherAuthors",numberOfDocsCitedByOtherAuthors)
        with open("output.csv", "a",encoding="utf-8") as fp:
            wr = csv.writer(fp, dialect='excel', lineterminator='\n')
            wr.writerow(list)
        self.final_doi_count+=1

    def main(self):
        list_doi=["10.1145/3368089.3409670",
        "10.1007/978-3-030-33702-5_1",
        "10.1109/SER-IP52554.2021.00009",
        "10.1109/ICSA47634.2020.00016",
        "10.1109/TSP49548.2020.9163501",
        "10.1109/SANER.2019.8667986",
        "10.35784/jcsi.2077",
        "10.1145/3357141.3357149",
        "10.1145/3178876.3186014",
        "10.1109/TR.2021.3101318",
        "10.4018/978-1-7998-2142-7.ch006",
        "10.1145/3372885.3373822",
        "10.1109/SER-IP52554.2021.00012",
        "10.1109/SER-IP52554.2021.00019",
        "10.1109/SER-IP52554.2021.00015",
        "10.1109/SER-IP52554.2021.00016",
        "10.1109/SER-IP52554.2021.00010",
        "10.1145/3437479.3437488",
        "10.1109/SER-IP52554.2021.00013",
        "10.1109/SER-IP52554.2021.00014",
        "10.1145/3356773.3356812",
        "10.1109/SER-IP52554.2021.00008",
        "10.1109/SER-IP52554.2021.00018",
        "10.5121/ijwsc.2020.11201",
        "10.1007/978-3-319-91662-0_5",
        "10.1016/j.jss.2020.110841",
        "10.26226/morressier.613b54401459512fce6a7ccb",
        "10.5220/0005500602770284",
        "10.5755/j01.itc.49.2.23757",
        "10.1109/ASE51524.2021.9678513",
        "10.13140/RG.2.2.33982.92488",
        "10.1109/AST52587.2021.00009",
        "10.1007/978-3-642-16120-9_15",
        "10.4018/978-1-7998-2531-9.ch005",
        "10.1109/SER-IP52554.2021.00017",
        "10.1109/DeepTest52559.2021.00008",
        "10.1109/ICST46399.2020.00023",
        "10.1007/978-90-481-3662-9_55",
        "10.1109/ASE51524.2021.9678513"]
        request="https://ieeexploreapi.ieee.org/api/v1/search/articles?index_terms=software&max_records=100&start_year=2015&end_year=2021&start_record=1&apikey=bz7esz8bu4zef4ye75bwuzvv"
        x=requests.get(request)
        list_doi.extend([item for item in [item['doi'] if 'doi' in item else 'xxx' for item in x.json()['articles']] if item != 'xxx'])
        time.sleep(4)
        request="https://ieeexploreapi.ieee.org/api/v1/search/articles?index_terms=machine+learning&max_records=100&start_year=2015&end_year=2021&start_record=1&apikey=bz7esz8bu4zef4ye75bwuzvv"
        x=requests.get(request)
        list_doi.extend([item for item in [item['doi'] if 'doi' in item else 'xxx' for item in x.json()['articles']] if item != 'xxx'])
        time.sleep(4)
        request="https://ieeexploreapi.ieee.org/api/v1/search/articles?index_terms=computer+vision&max_records=100&start_year=2015&end_year=2021&start_record=1&apikey=bz7esz8bu4zef4ye75bwuzvv"
        x=requests.get(request)
        list_doi.extend([item for item in [item['doi'] if 'doi' in item else 'xxx' for item in x.json()['articles']] if item != 'xxx'])
        df1 = pd.read_csv('./scopus_dois_csvs/ACM Computing Surveys.csv')
        df2 = pd.read_csv('./scopus_dois_csvs/IEEE Transactions on Cybernetics.csv')
        # df3 = pd.read_csv('./scopus_dois_csvs/IEEE Transactions on Network and Service Management.csv')
        df4 = pd.read_csv('./scopus_dois_csvs/International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS.csv')
        # df5 = pd.read_csv('./scopus_dois_csvs/Proceedings of the ACM Conference on Computer and Communications Security.csv')
        df6 = pd.read_csv('./scopus_dois_csvs/Proceedings of the ACM SIGMOD International Conference on Management of Data.csv')
        df7 = pd.read_csv('./scopus_dois_csvs/Proceedings of the Annual ACM Symposium on Principles of Distributed Computing.csv')
        # df8 = pd.read_csv('./scopus_dois_csvs/Proceedings of the IEEE International Conference on Computer Vision.csv')
        df1_doi=df1["DOI"]
        df2_doi=df2["DOI"]
        # df3_doi=df3["DOI"]
        df4_doi=df4["DOI"]
        # df5_doi=df5["DOI"]
        df6_doi=df6["DOI"]
        df7_doi=df7["DOI"]
        # df8_doi=df8["DOI"]
        array_dfs=[df1_doi,df2_doi,df4_doi,df6_doi,df7_doi]
        df = pd.concat(array_dfs)
        arr=df.values.tolist()
        list_doi.extend(arr)
        for doi in tqdm(list_doi):
            self.get_metrics(doi)
        page_rank=calculate_page_rank(self.final_doi_count,self.references, self.main_paperid)
        with open('output.csv', 'r') as read_obj, \
            open('output_1.csv', 'w', newline='') as write_obj:
            # Create a csv.reader object from the input file object
            csv_reader = csv.reader(read_obj)
            # Create a csv.writer object from the output file object
            csv_writer = csv.writer(write_obj)
            # Read each row of the input csv file as list
            i=0
            firstRow=True
            for row in csv_reader:
                if firstRow:
                    firstRow=False
                    row.append("PageRank")
                    csv_writer.writerow(row)
                    continue
                # Append the default text in the row / list
                row.append(page_rank[i])
                # Add the updated row / list to the output file
                csv_writer.writerow(row) 
                i+=1

c=calc()
c.main()

    



    



