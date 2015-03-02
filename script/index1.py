#!/usr/bin/env python

from datetime import datetime
# load name data
def load_name_sample(input,isTest):
    f = open(input)
    y = []
    x = []
    max_feature = 0
    field_cnt = 0
    line = f.readline()
    index = 3
    if isTest == True:
        index = 2
    cnt = 0
    
    while True:
        line = f.readline()
        if line.strip()=="" :
            break
        fields = line.split(',')
        if isTest == False:
            label = int(fields[1])
            if label == 0:
                label = -1
            y.append(label)
        else:
            y.append(-1)
     
        cur_x = []
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
            idx = d.get(fields[i])
            if idx == None:
                cur_x.append(len(d))
                d[fields[i]] = len(d)
            else:
                cur_x.append(idx)
        cur_str_x = [str(x) for x in cur_x]
        if isTest == True:
            print >> fm_test,str(y[cnt])+" "+" ".join(cur_str_x)
        else:
            print >> fm_train,str(y[cnt])+" "+" ".join(cur_str_x)
        cnt = cnt + 1
        if cnt % 1000000 == 0:
            print cnt

starttime = datetime.now()

d = {}

fm_train = open("../fm_train_1","w")
fm_test = open("../fm_test_1","w")

load_name_sample('../train_pre',False)
load_name_sample('../test_pre',True)

fm_train.close()
fm_test.close()

#learner = field_fm(k,l,t,alpha,beta,max_feature,field_cnt)
endtime = datetime.now()
print (endtime-starttime).seconds