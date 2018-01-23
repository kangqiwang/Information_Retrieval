# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 20:55:44 2017

@author: Kangqi
"""
#from sklearn.metrics import jaccard_similarity_score
from pandas import DataFrame
import pandas as pd
import jellyfish as jf
import operator
import matplotlib.pyplot as plt
import matplotlib.image as mpimg  
from lxml import etree
import math
import numpy as np

class Basic:
    __location="E:\Computer Science\informatics\coursework\cmt209-coursework-2017\image_tags.csv"
    __image_tags= DataFrame()
    __primitive_input=''
    __string_processed=[]

    def __init__(self):
        self.__primitive_input=input("input your keyword:")
    
        
        # read csv file to image_tag
    def csv_data(self):
        self.__image_tags=pd.read_csv(self.__location)

    #for caculate jaro_distance using jellyfish
    #get similarity and if conditional sentence ,fuzzy string match
    def string_similarity(self,name_row,string_processed_buffer,fuzzy_buffer,y):
        for x in name_row:
            fuzzy=jf.jaro_distance(x, y)
            if fuzzy<0.90:
                continue
            # jaro_distance() user input wrong
            if fuzzy>0.95:
                self.__string_processed.append(x)
                return 
            if fuzzy>=0.90 and fuzzy<=0.95 and not(y in self.__string_processed):
                string_processed_buffer.append(x+' '+y)
                fuzzy_buffer.append(fuzzy)
        
        #change the string which we need change, if between 0.90 to 0.95
        #mention user have something wrong
    def string_s_all(self,name_row,string_input):
        string_processed_buffer=[]
        fuzzy_buffer=[]
        for y in string_input:
            self.string_similarity(name_row,string_processed_buffer,fuzzy_buffer,y)
            if (y in self.__string_processed) and ([]==len(string_processed_buffer)):
                string_processed_buffer.pop()
                fuzzy_buffer.pop()
        self.__string_processed=list(set(self.__string_processed))
        return (string_processed_buffer,fuzzy_buffer,name_row)




    #finish the string similarity 
    def string_processed(self):
        string_input=self.__primitive_input.split(' ')
        
        string_input=[element.lower() for element in string_input]
        name_row=self.__image_tags.columns.get_values().tolist()
        name_row=[element.lower() for element in name_row]
        del name_row[0]
        return (name_row,string_input)
            
        #one of similarity function, it is not default similarity function
        #can use it in task2 and task3
    def cosine_similarity(self,v1,v2):
        sumxx, sumxy, sumyy = 0, 0, 0
        for i in range(len(v1)):
            x = v1[i]; y = v2[i]
            sumxx += x*x
            sumyy += y*y
            sumxy += x*y
        return (sumxy/math.sqrt(sumxx*sumyy))
    # one of tthe similarity function, it is default one,
    #it is easy to calculate
    def jaccard(self,x,y):
        x = np.asarray(x, np.bool) 
        y = np.asarray(y, np.bool) 
        return np.double(np.bitwise_and(x, y).sum()) / np.double(np.bitwise_or(x, y).sum())
    # the function is for caculate the similarity
    # return the list of sim
    def similarity(self,name_row):
        
        a_data = [None] * 58
        
        for j in range(len(self.__string_processed)): 
            for i in range(len(name_row)) :
                if name_row[i]==self.__string_processed[j]:
                    a_data[i]=1
                elif not a_data[i]==1:
                    a_data[i]=0
                
        my_data=[]
        #b_data=[None]*58
        my_jaccard=[]
        i=0
        
        while i<=499:
            my_data=self.__image_tags.loc[i].tolist()
            del my_data[0]
           # deprecated jaccard_similarity my_jaccard.append(jaccard_similarity_score(a_data,my_data))
           # deprecated cosine_similarity
            my_jaccard.append(self.jaccard(a_data,my_data))
            i+=1
        return my_jaccard
    # the function is based on the similarity to rank
    def similarity_ranking(self,my_jaccard):
        rank=list(range(0, 500))
        dictionary=dict(zip(rank,my_jaccard))
        sorted_x = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
        result_list=[]
        name_list=[]
        all_result=[]
        i=0
        while i<480:
            del sorted_x[-1]
            i+=1
        for x in sorted_x:
            mylist=list(x)
            result_list.append(mylist[0])
            name_list.append(self.__image_tags.loc[mylist[0],'name'])
        all_result=list(zip(name_list,sorted_x))
        
            
        return all_result,name_list

            
        #function output the the result
    def output_result(self,all_result,name_list):
        nam1_list=[]
        jac_list=[]
        for x in range(20):
            temp=list(all_result[x])      
            tem1=list(temp[1])
            del tem1[0]
            jac_list.append(tem1)
            del temp[1]
            nam1_list.append(temp)
            
            print(nam1_list[x],'\t',jac_list[x])
        for x in name_list:
            imagePath='E:\\Computer Science\\informatics\\cmt209-coursework-2017\\images\\'+x+'.png'
            img = mpimg.imread(imagePath)
            plt.imshow(img)
            plt.show()  
        

    # if user inputed string , the program can identify, output ask user           
    def out_put_voc(self,string_processed_buffer,fuzzy_buffer):
        if len(string_processed_buffer):
            print('sorry, what do you mean?')
            print(string_processed_buffer)
            print(fuzzy_buffer)
        
        else:
            print('successfully')
        return self.__string_processed
    """
   for############  task2 b      ##########start to pic similarity, jaccard similarity 
    
    """
class Advanced(Basic):
    __location="E:\Computer Science\informatics\coursework\cmt209-coursework-2017\image_tags.csv"
    __image_tags= DataFrame()
    __primitive_input=''
    __string_processed=[]
    __synonym_location='E:\Computer Science\informatics\coursework\cmt209-coursework-2017\\new.csv'
    __synonym=DataFrame()
    #read the csv file
    def csv_data(self):
        Basic.csv_data(self)
        self.__image_tags=pd.read_csv(self.__location)

        self.__synonym=pd.read_csv(self.__synonym_location)

    # for check the Synonyms, if have synonyms, as user input the original word
    def string_processed(self):
        name_row,string_input=Basic.string_processed(self)
        result=[]
        for i in range(len(string_input)):
            #synonyms
            for x in range(1,5):
                for y in range(0,17):
                    if string_input[i]==self.__synonym.iloc[y,x]:
                        result.append(name_row[y])
            #concepts higher up in the hierarchy
            hierarchy_loc='E:\Computer Science\\informatics\\finished\\hierarchy.csv'
            hierarchy=pd.read_csv(hierarchy_loc)
            data=''
            save_data=[]
            for x in string_input:
                try:
                    data+=(hierarchy[x][0])
                except:
                    save_data.append(x)

            try:
                child_input=data.split(' ')
                result+=child_input
            except:
                result=string_input
            result+=save_data
            return (name_row,result,string_input)
        
        #before rank the picture based on similarity,
        #the program read the xml file and detect whether the word have parent node
        #if it have parent, check if the parent have other children, if the
        # answer is yes, +0.01 for every its brother node in similarity
    def similarity_ranking(self,my_jaccard,result,string_input,name_row):
            file_name=['creature','weather','grocery','activity','accessory','weather']
            find_tag=[]
            cos_sim=my_jaccard
            for x in file_name:
                hierarchy_loc='E:\Computer Science\\informatics\\finished\\'+x+'.xml'    
                tree = etree.parse(hierarchy_loc)
                child_number=[]
                
                for i in string_input:
                    save_tag=[]
                    try:
                        save_tag=tree.xpath('.//'+i)[0]
                        if not len(save_tag.tag)==0:
                            app=list(save_tag.getparent())
                            if len(app)>=1:
                                for j in range(len(app)):
                                    if not app[j].tag==i:
                                        #just 1 distance
                                        for a in name_row:
                                            if app[j].tag==a:
                                                child_number.append(len(app))
                                                find_tag.append(app[j].tag)
                    except:
                        pass
                        

            #just have distance 1
            for x in find_tag:
                index=[]
                apple=list(self.__image_tags[x])
                for x in range(len(apple)):
                    if apple[x] ==1:
                        index.append(x)
                for y in index:
                    #jaccard +0.01
                    my_jaccard[y]+=0.01
            all_result,name_list=Basic.similarity_ranking(self,my_jaccard)
            return (all_result,name_list,cos_sim)


                        
            
        
    
#   task 2 (b)

ad= Advanced()
ad.csv_data()
name_row,result,string_input=ad.string_processed()

string_processed_buffer,fuzzy_buffer,name_row=ad.string_s_all(name_row,result)
my_jaccard=ad.similarity(name_row)
all_result,name_list,cos_sim=ad.similarity_ranking(my_jaccard,result,string_input,name_row)
ad.output_result(all_result,name_list)

'''
task 2 (a)
'''
'''
basic= Basic()
basic.csv_data()
name_row,string_input=basic.string_processed()

string_processed_buffer,fuzzy_buffer,name_row=basic.string_s_all(name_row,string_input)
my_jaccard=basic.similarity(name_row)
all_result,name_list=basic.similarity_ranking(my_jaccard)
basic.output_result(all_result,name_list)

data=basic.out_put_voc(string_processed_buffer,fuzzy_buffer)
'''
        
    
    
        
        
                
    