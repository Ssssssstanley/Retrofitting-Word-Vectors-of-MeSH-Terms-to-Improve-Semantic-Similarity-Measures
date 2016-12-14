##
import urllib
import os
import random
import csv
#from processData import Process
#import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from Bio import Medline
from Bio import Entrez
import math
import numpy as np
import matplotlib.pyplot as plt
Entrez.email = 'zhiguo.yu@uth.tmc.edu'

def queryPubMed(mesh, docpath):
    if not os.path.isdir(docpath):
        os.makedirs(docpath)
    if len(mesh)>1:
        query = '"'+mesh[0]+'"[MeSH Terms]'+' OR '+'"'+mesh[1]+'"[MeSH Terms]'
    else:
        query = '"'+mesh[0]+'"[MeSH Terms]'
    print query
    esearch = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&mindate=1945&maxdate=2016&retmode=xml&retmax=10000000&term=%s' % (query)
    handle = urllib.urlopen(esearch)
    data = handle.read()
    #print data
    root = ET.fromstring(data)
    ids = [x.text for x in root.findall("IdList/Id")]
    ## random choose 10,100,1000 docs five times
    
    # 10 docs
    print 'Got %d articles' % (len(ids))
    '''print 'Randomly Retrieving 10 docs five times'
    for j in range(5):
        print j
        f1 = open(docpath+'/docs_10_'+str(j)+'.txt','w')
        f2 = open(docpath+'/meshes_10_'+str(j)+'.txt','w')
        idlist = random.sample(ids,10)
        handle = Entrez.efetch(db="pubmed",id=idlist,rettype="medline",retmode="text")
        records = Medline.parse(handle)
        records = list(records)
        for record in records:
            if record.get("MH",""):
                for item in record.get("MH",""):
                    f2.writelines(item)
                    f2.write('|')
                f2.write("\n")
                f1.writelines(record.get("TI",""))
                f1.writelines(record.get("BTI",""))
#                print "Abstract:",record.get("AB","")
                f1.writelines(record.get("AB",""))
                f1.write("\n")
        f1.close()
        f2.close()
            
    # 100 docs
    print 'Randomly Retrieving 100 docs five times'
    for j in range(5):
        print j
        f1 = open(docpath+'/docs_100_'+str(j)+'.txt','w')
        f2 = open(docpath+'/meshes_100_'+str(j)+'.txt','w')
        idlist = random.sample(ids,100)
        handle = Entrez.efetch(db="pubmed",id=idlist,rettype="medline",retmode="text")
        records = Medline.parse(handle)
        records = list(records)
        for record in records:
            if record.get("MH",""):
                for item in record.get("MH",""):
                    f2.writelines(item)
                    f2.write('|')
                f2.write("\n")
                f1.writelines(record.get("TI",""))
                f1.writelines(record.get("BTI",""))
#                print "Abstract:",record.get("AB","")
                f1.writelines(record.get("AB",""))
                f1.write("\n")
        f1.close()
        f2.close()'''
            
    # 1000 docs
    print 'Randomly Retrieving 3000 docs five times'
    for j in range(5):
        print j
        f1 = open(docpath+'/docs_3000_'+str(j)+'.txt','w')
        f2 = open(docpath+'/meshes_3000_'+str(j)+'.txt','w')
        idlist = random.sample(ids,3000)
        for sub_id in range(0,3000,100):
            
            handle = Entrez.efetch(db="pubmed",id=idlist[sub_id:sub_id+100],rettype="medline",retmode="text")
            records = Medline.parse(handle)
            records = list(records)
            for record in records:
                if record.get("MH",""):
                    for item in record.get("MH",""):
                        f2.writelines(item)
                        f2.write('|')
                    f2.write("\n")
                    f1.writelines(record.get("TI",""))
                    f1.writelines(record.get("BTI",""))
    #                print "Abstract:",record.get("AB","")
                    f1.writelines(record.get("AB",""))
                    f1.write("\n")
        f1.close()
        f2.close()
                
    
    
def query_MeSH():
    
    meshes =[]
    for line in open('mapped_mesh_pairs.txt','r'):
        line = line.strip().split(':')
        for item in line:
            if item not in meshes:
                if '/' in item:
                    meshes.append(item.split('/'))
                else:
                    meshes.append([item])
    for mesh in meshes:
        print mesh
        docpath = './'+str(mesh)
        queryPubMed(mesh, docpath)

query_MeSH()
    
    
    