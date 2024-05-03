import spacy
from spacy import displacy
from spacy.training import Example
import random
import pandas as pd
from spacy.util import minibatch, compounding
from spacy.matcher import Matcher


class recognizer:
    def __init__(self,n):
        self.nlp = n
        self.matcher = Matcher(self.nlp.vocab)
        self.train()

    def train(self):
      batchsize = 10
      data = ["INCIDENT_NUMBER","OFFENSE_CODE","OFFENSE_DESCRIPTION","DISTRICT","REPORTING_AREA",
              "OCCURRED_ON_DATE","YEAR","MONTH","DAY_OF_WEEK","HOUR","STREET"]
#, "Image-URL-L"]

      self.train_data = []
      counter = 0
      
      for batches in pd.read_csv("crime.csv",chunksize=batchsize):
            #print(batches)
           
            for row in batches.itertuples(index=False):
                    #print(row)
                    label_reqd = str(row.INCIDENT_NUMBER).lower() + "||" + str(row.OFFENSE_CODE).lower() + "||" + str(row.OFFENSE_DESCRIPTION).lower() + "||" + \
                    str(row.DISTRICT).lower() + "||" + str(row.REPORTING_AREA).lower() + "||" + str(row.OCCURRED_ON_DATE).lower() + "||" + str(row.YEAR).lower() + \
                        "||" + str(row.MONTH).lower() + "||" +str(row.DAY_OF_WEEK).lower() + "||" + str(row.HOUR).lower() + "||" + str(row.STREET).lower()

                    pattern_reqd = str(row.OFFENSE_CODE).lower()
                    pattern_reqd = pattern_reqd.split()

                    pattern = [{"lower":word,"OP": "*"} for word in pattern_reqd]
            
                    self.matcher.add(label_reqd,[pattern])
          
        
        

          
      #self.recognize(text = "Classical Mythology", remove = 1)# remove stop words
    def recognize(self,text, remove):

        doc = self.nlp(text.lower())
        if remove == 1:
            print('StopWordds removed')
            doc = spacy.tokens.Doc(self.nlp.vocab, words=[token.text for token in [token for token in doc if not token.is_stop]])
        matches = self.matcher(doc)

        self.high_temp = []
        self.temp = set()
        #print("DOC: ",doc)
        for match_id, start, end in matches:
            matched_span = doc[start:end]
            label = self.matcher.vocab.strings[match_id]
            #print("LABEL: ",label)
            c = 0
            for word in doc:
               #print("..........",word.text,label)
               if word.text in label:
                  c += 1

            if c == len(doc):
               print(label,c)
               if not label in self.high_temp:
                    #print("IN")
                    self.high_temp.append(label)
            else:
                self.temp.add(label)
            #max_c = 0
            #cnt,book = filter()
            
        if  self.temp == set() and self.high_temp == []:
            print('No result. Redoing')
            self.recognize(text, remove = 0) #dont remove stop words

        
        if self.high_temp == []:
            for books in self.temp:         
                yield(books)

        else:
            for books in self.high_temp:
                yield(books)



        #self.high_priority()

    # def high_priority(self):
    #     for books in self.high_temp:
    #         yield(books)

    # def low_priority(self):
    #     for books in self.temp:
    #         yield(books)
            
if __name__ == "__main__":
    nlp = spacy.load("en_core_web_lg")
    recognizer(nlp)