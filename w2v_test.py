## test retrofit
import gensim
import logging as log
import nltk



def main():
    cuis = []
    for line in open('./drug_review/drug_cuis.txt','r'):
        line = line.strip().split('|')[1].split(',')
        cuis.append(line)
    docpath = '/Users/zyu4/Documents/Research/word2vec/w2v'    
    model = gensim.models.Word2Vec.load_word2vec_format(docpath+'/w2v-model-PubMed-CUIs.bin', binary=True)
    
    for items in cuis:
        for item in items:
            try:
                print model.similarity(item,item)
                
            except:
                print item
main()



