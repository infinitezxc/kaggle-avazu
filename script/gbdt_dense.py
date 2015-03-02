#!/usr/bin/env python

# generate dense feature for gbdt
from datetime import datetime
import marshal

id_stat =  marshal.load(open("../id_stat"))

# load name data
def load_name_sample(input,isTest):
    f = open(input)
    y = []
    x = []
    line = f.readline()
    index = 3
    if isTest == True:
        index = 2
    cnt = 0
    isValid = False
    
    while True:
        line = f.readline().strip()
        if not line :
            break
        fields = line.split(',')
        if isTest == False:
            label = int(fields[1])
            if label == 0:
                label = -1
            y.append(label)
            if isValid==False:
                if int(fields[2][4:6]) > 28:
                    isValid = True
        else:
            y.append(-1)
     
        cur_x = []
        for i in xrange(index,len(fields)):
            if i == len(fields)-19:
                cur_x.append(id_stat["j_"+fields[i]])
                #continue
            elif i == len(fields)-20:
                #cur_x.append(gbdt_id["i_"+fields[i]])
                continue
            elif i == len(fields)-7:
                cur_x.append(id_stat["v_"+fields[i]])
            elif i > len(fields)-7:
                cur_x.append(int(fields[i]))

        cur_str_x = [str(x) for x in cur_x]
        if isTest == True:
            print >> gbdt_test,str(y[cnt])+" "+" ".join(cur_str_x)
        else:
            print >> gbdt_train,str(y[cnt])+" "+" ".join(cur_str_x)
        cnt = cnt + 1
        if cnt % 1000000 == 0:
            print cnt

starttime = datetime.now()

d = {}

gbdt_train = open("../train_dense","w")
gbdt_test = open("../test_dense","w")

load_name_sample('../train_c',False)
load_name_sample('../test_c',True)

gbdt_train.close()
gbdt_test.close()

#learner = field_fm(k,l,t,alpha,beta,max_feature,field_cnt)
endtime = datetime.now()
print (endtime-starttime).seconds