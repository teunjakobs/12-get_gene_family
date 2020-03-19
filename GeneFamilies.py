import requests
from prody import *
from matplotlib.pylab import *
import re

#This script will query uniprot for homo sapiens with a given gene symbol
#It then uses the uniprot ID to query pfam to find corresponding families to the gene symbol.

class Gene:
    def __init__(self,symbol,family):
        self.symbol = symbol
        self.family = family

my_genes = []
for i in range(1):
    my_genes.append(Gene("P53",""))
    my_genes.append(Gene("BRCA1",""))

#function to search uniprot with variable query (given in next function)
def search_uniprot(query,format = 'txt'):
    base_url = 'https://www.uniprot.org/uniprot'
    payload = {'query':query, 'format':format}
    result = requests.get(base_url,params = payload)
    if result.ok:
        return result.content
    else:
        print('Error')

fam_dict = {}

#Fucntion to query uniprot and use uniprot id to query pfam
def query(fam_dict):
    for gene in my_genes:
        query = "organism:homo sapiens and gene_exact: " + gene.symbol
        res = search_uniprot(query) #search uniprot using above query
        info = res.decode()  #bytes before decoding
        uniprot_id = info.strip().split("\n")
        uniprot_id = uniprot_id[1].split()
        uniprot_id = uniprot_id[1].replace(";","")

        #pfam part
        ion()  #turn interactive mode on
        matches = searchPfam(uniprot_id) #query pfam with uniprot ID

        fam_dict[gene.symbol] = []
        for i in matches.keys(): #reaching the keys of dict
            fam = matches[i].get('id') #reaching every element in tuples
            fam_dict[gene.symbol].append(fam)

    return fam_dict

#Add family to each gene symbol
def add_fam(fam_dict):
    for k, v in fam_dict.items():
        for gene in my_genes:
            if k == gene.symbol:
                gene.family = str(v)

    for gene in my_genes:
        print(gene.symbol + ": " + gene.family)

fam_dict = query(fam_dict)
add_fam(fam_dict)
