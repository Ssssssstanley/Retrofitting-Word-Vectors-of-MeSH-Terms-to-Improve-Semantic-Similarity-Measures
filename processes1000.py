##
from processData import Process
import numpy as np
import csv
import math
import scipy.stats
import os
import time
# get each mesh's words distribution
def process_mesh(D, ranIndex,mesh):
    mesh = str(mesh)
    data = ''
    for line in open('./'+mesh+'/docs_'+str(D)+'_'+str(ranIndex)+'.txt','r'):
        data = data+' '+line.strip()
    p1 = Process()
    tokens = p1.compute_documents(data)
    [s2, words] = p1.stopwords(tokens)
    
    word_df ={}
    for line in open('./'+mesh+'/docs_'+str(D)+'_'+str(ranIndex)+'.txt','r'):
        p = Process()
        doc_tokens = p.compute_documents(line.strip())
        for token in set(doc_tokens):
            word_df[token] = word_df.get(token,0)+1
    
    word_tfidf={}
    WOs =[]
    for item in s2:
        if item[0] in word_df:
            word_tfidf[item[0]]=item[1]*math.log(1.0*D/word_df[item[0]])
            WOs.append(item[0])  
    return [word_tfidf, WOs]

def cosine(M1,M2):
    nor = sum([a*b for a, b in zip(M1, M2)])
    denor = math.sqrt(sum([math.pow(i,2) for i in M1]))*math.sqrt(sum([math.pow(j,2) for j in M2]))
    return (nor*1.0)/denor


def compute_sim(dic1, dic2, WOs1, WOs2):
    vec1 = []
    vec2 = []
    for word in set(WOs1+WOs2):
        vec1.append(dic1.get(word,0.0))
        vec2.append(dic2.get(word,0.0))
    return cosine(vec1, vec2)
    

def compare_mesh():
    meshes =[]
    for line in open('mapped_mesh_pairs.txt','r'):
        line = line.strip().split(':')
        tmp =[]
        for item in line:
            if '/' in item:
                tmp.append(item.split('/'))
            else:
                tmp.append([item])
        meshes.append(tuple(tmp))
    D=100
    simscores=[]
    j=0
    for mesh_pair in meshes:
        j +=1
        print j
        print mesh_pair
        score = 0
        if mesh_pair[0]==mesh_pair[1]:
            simscores.append(1.00)
            print '1.0'
        else:
            for i in range(5):
                [word_tfidf1, WOs1]= process_mesh(D, i,mesh_pair[0])
                [word_tfidf2, WOs2]= process_mesh(D, i,mesh_pair[1])
                score +=compute_sim(word_tfidf1, word_tfidf2, WOs1, WOs2)
            print score/5.0  
            a = str(score/5.0)
            if a[4]>='5':
                a = float(a[:4])+0.01
            simscores.append(a)
               
    return simscores

def get_gs_rank():
    ## get physicians' rank
    '''phy_rank={}
    for line in open('./MiniMayoSRS.msh.physicians','r'):
        line = line.strip().split('<>')
        phy_rank[tuple([line[1],line[2]])] = float(line[0])
    ## get coder's rank
    cod_rank={}
    for line in open('./MiniMayoSRS.msh.coders','r'):
        line = line.strip().split('<>')
        cod_rank[tuple([line[1],line[2]])] = float(line[0])
    
    ## get 25 MeSH pairs
    ranking_phy=[]
    ranking_coder=[]
    
    for line in open('./MiniMayoSRS.msh.cuis','r'):
        line = line.strip().split('<>')
        ranking_phy.append(phy_rank[tuple([line[0],line[1]])])
        ranking_coder.append(cod_rank[tuple([line[0],line[1]])])'''
    phy_rank={}
    coder_rank={}
    with open('./MiniMayoSRS.csv','rb') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            phy_rank[tuple([row[4], row[5]])] = float(row[0])
            coder_rank[tuple([row[4], row[5]])] = float(row[1])
    ranking_phy=[]
    ranking_coder=[]
    for line in open('./mesh_pairs','r'):
        line =line.strip().split(',')
        ranking_phy.append(phy_rank[tuple([line[0],line[1]])])
        ranking_coder.append(phy_rank[tuple([line[0],line[1]])])
    
    return [ranking_phy, ranking_coder]

def process_doc_mesh(D, ranIndex, mesh):
    mesh_doc_cnt={}
    mesh_docs={}
    c = 0
    for line in file('./'+str(mesh)+'/meshes_'+str(D)+'_'+str(ranIndex)+'.txt','r'):
        mesh_tep=[]
        for item in line.strip().split('|'):
            if len(item)>1:
                item = item.replace('*','')
                if '/' in item:
                    mesh_tep.append(item.split('/')[0])
                        
                else:
                    mesh_tep.append(item)
        for item1 in set(mesh_tep):
            mesh_doc_cnt[item1] =mesh_doc_cnt.get(item1,0)+1
            if item1 in mesh_docs:
                mesh_docs[item1].append(c)
            else:
                mesh_docs[item1]=[c]
        c +=1
    return [mesh_doc_cnt, mesh_docs]

def copute_umls_sim(D,ranIndex, mesh):
    [mesh_doc_cnt, mesh_docs] = process_doc_mesh(D, ranIndex, mesh)
    f = open('./'+mesh+'/mesh_pairs_'+str(D)+'_'+str(ranIndex)+'.txt','w')
    for item in mesh_doc_cnt:
        if mesh_doc_cnt[item] >=0.5*D:
            f.writelines(mesh+'<>'+item)
            f.write('\n')
    return 0

def test_mesh_sim():
    meshes =[]
    for line in open('mapped_mesh_pairs.txt','r'):
        line = line.strip().split(':')
        tmp =[]
        for item in line:
            if '/' in item:
                tmp.append(item.split('/'))
            else:
                tmp.append([item])
        meshes.append(tuple(tmp))
    D=100
    j = 0
    for mesh_pair in meshes:
        j+=1
        print j
        print mesh_pair
        if mesh_pair[0]==mesh_pair[1]:
            continue
        else:
            for mesh in mesh_pair:
                if len(mesh)==1:
                    continue
                    '''for i in range(5):
                        print mesh, mesh_pair
                        [mesh_doc_cnt, mesh_docs] = process_doc_mesh(D, i, mesh)
                        docpath = './['+mesh[0]+']'
                        if not os.path.isdir(docpath):
                            os.makedirs(docpath)
                        f = open(docpath+'/mesh_pairs_'+str(D)+'_'+str(i)+'.txt','w')

                        print len(mesh_doc_cnt)

                        for item in mesh_doc_cnt:
                            if item != mesh[0]:
                                if mesh_doc_cnt[item] >0.1*D:
                                    f.writelines(mesh[0]+'<>'+item)
                                    f.write('\n')
                        f.close()
                        #time.sleep(5)
                        os.system('perl query-umls-similarity-webinterface.pl --sab MSH --measure lch --infile '+'./'+str(mesh)+'/mesh_pairs_'+str(D)+'_'+str(i)+'.txt'+' --outfile '+'./'+str(mesh)+'/lch_score_'+str(D)+'_'+str(i)+'.txt')
                        '''
                else:
                    if ' 'in mesh[0]:
                        continue
                        for i in range(5):
                            print mesh, mesh_pair
                            [mesh_doc_cnt, mesh_docs] = process_doc_mesh(D, i, mesh)
                            
                            docpath = './['+mesh[0].replace(' ','_')+']'
                            if not os.path.isdir(docpath):
                                os.makedirs(docpath)
                            f = open(docpath+'/mesh_pairs_'+str(D)+'_'+str(i)+'.txt','w')
                            for sub_mesh in mesh:
                                for item in mesh_doc_cnt:
                                    if item != mesh[0]:
                                        if mesh_doc_cnt[item] >0.1*D:
                                            f.writelines(sub_mesh+'<>'+item)
                                            f.write('\n')
                            f.close()
                            os.system('perl query-umls-similarity-webinterface.pl --sab MSH --measure lch --infile '+'./['+mesh[0].replace(' ','_')+']/mesh_pairs_'+str(D)+'_'+str(i)+'.txt'+' --outfile '+'./['+mesh[0].replace(' ','_')+']/lch_score_'+str(D)+'_'+str(i)+'.txt')
                    else:
                        for i in range(5):
                            print mesh, mesh_pair
                            [mesh_doc_cnt, mesh_docs] = process_doc_mesh(D, i, mesh)
                            
                            docpath = './['+mesh[0]+']'
                            if not os.path.isdir(docpath):
                                os.makedirs(docpath)
                            f = open(docpath+'/mesh_pairs_'+str(D)+'_'+str(i)+'.txt','w')
                            for sub_mesh in mesh:
                                for item in mesh_doc_cnt:
                                    if item != mesh[0]:
                                        if mesh_doc_cnt[item] >0.1*D:
                                            f.writelines(sub_mesh+'<>'+item)
                                            f.write('\n')
                            f.close()
                            os.system('perl query-umls-similarity-webinterface.pl --sab MSH --measure lch --infile '+'./['+mesh[0]+']/mesh_pairs_'+str(D)+'_'+str(i)+'.txt'+' --outfile '+'./['+mesh[0]+']/lch_score_'+str(D)+'_'+str(i)+'.txt')

                                            
                                    
    return 0
    

def main():
    simscores = compare_mesh()
    [ranking_phy, ranking_coder] = get_gs_rank()
    print len(simscores),len(ranking_phy),len(ranking_coder)
    print scipy.stats.spearmanr(simscores, ranking_phy)
    print scipy.stats.spearmanr(simscores, ranking_coder)
    print scipy.stats.spearmanr(ranking_coder, ranking_phy)
#main()
test_mesh_sim()
    