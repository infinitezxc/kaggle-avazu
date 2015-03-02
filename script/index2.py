#!/usr/bin/env python
from datetime import datetime

# load name data
def load_name_sample(input,isTest):
    f = open(input)
    y1 = []
    x1 = []
    y2 = []
    x2 = []
    lable1 = []
    label2 = []
    max_feature = 0
    field_cnt = 0
    line = f.readline()
    index = 3
    if isTest == True:
        index = 2
    cnt = 0

    label = -1
    id = "??"

    d = {}
    while True:
        isApp = False
        line = f.readline()
        if line.strip()=="" :
            break
        fields = line.split(',')
        id = fields[0]
        if isTest == False:
            label = int(fields[1])
            if label == 0:
                label = -1
        cur_x = []
        
        if fields[index+2] == "c_85f751fd":
            isApp = True
            d = d_app
        else:
            d = d_site

        for i in xrange(index,len(fields)):            
            if i == len(fields)-2:
                ss = fields[i].split('_')
                if int(ss[1])>=50:
                    fields[i]=ss[0]+"_50"
            elif i == len(fields)-5:
                ss = fields[i].split('_')
                if int(ss[1])>=20:
                    fields[i]=ss[0]+"_20"
            elif i > len(fields)-8 and i < len(fields)-1:
                ss = fields[i].split('_')
                if int(ss[1])>=10:
                    fields[i]=ss[0]+"_10"
            
            if isApp == True:
                if fields[i][0] == "d" or fields[i][0] == "e" or fields[i][0] == "c":
                    continue
            else:
                if fields[i][0] == "g" or fields[i][0] == "h" or fields[i][0] == "f": 
                    continue
                
            idx = d.get(fields[i])
            if idx == None:
                cur_x.append(len(d))
                d[fields[i]] = len(d)
            else:
                cur_x.append(idx)
        cur_str_x = [str(x) for x in cur_x]
        if isApp == False:
            if isTest == True:
                print >> fm_test_1,str(label)+" "+" ".join(cur_str_x)
            else:
                print >> fm_train_1,str(label)+" "+" ".join(cur_str_x)
        else:
            if isTest == True:
                print >> fm_test_2,str(label)+" "+" ".join(cur_str_x)             
            else:
                print >> fm_train_2,str(label)+" "+" ".join(cur_str_x)
        cnt = cnt + 1
        if cnt % 100000 == 0:        
            print cnt
		

starttime = datetime.now()

d_app = {}
d_site = {}

fm_train_1 = open("../fm_train_1_1","w")
fm_test_1 = open("../fm_test_1_1","w")
fm_train_2 = open("../fm_train_1_2","w")
fm_test_2 = open("../fm_test_1_2","w")

load_name_sample('../train_pre',False)
load_name_sample('../test_pre',True)

fm_train_1.close()
fm_test_1.close()
fm_train_2.close()
fm_test_2.close()

endtime = datetime.now()

print (endtime-starttime).seconds