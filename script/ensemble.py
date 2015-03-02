import math
from pprint import pprint
from calibrate import calibrate

inputs = ["lr_c1_cal.txt","ftrl_c5_cal.txt"]
label = ""
output_file = "./ensemble1.txt"

def cal_weights(weights):
    r = []
    sum = 0.0
    for w in weights:
        sum += w
    for w in weights:
        r.append(w/sum)
    return r
    
def get_pred_ctr(input):
    f = open(input)
    ctr = []
    while True:
        line = f.readline().strip()
        if not line:
            break
        ctr.append(float(line))
    f.close()
    return ctr

def ensemble(weights,files,output):
    ctrs = []
    weights = cal_weights(weights)
    f = open(output,"w")
    for file in files:
        ctr = get_pred_ctr(file)
        print "loading "  + file
        ctrs.append(ctr)
    sample_num = len(ctrs[0])

    for j in xrange(sample_num):
        cur_ctr = 0.0
        for k in xrange(len(ctrs)):
            cur_ctr += weights[k] * math.log(ctrs[k][j]/(1-ctrs[k][j]))
        cur_ctr = 1/(1+math.exp(-cur_ctr))
        print >> f, str(cur_ctr)
    f.close()

def sub(result,testfile,output):
    f = open(testfile)
    r = open(result)
    o = open(output,"w")
    l1 = f.readline()
    print >> o, "id,click"
    while True:
        l1 = f.readline()
        l2 = r.readline().strip()
        if not l1:
            break
        print >> o, l1.split(',')[0]+","+l2
    f.close()
    r.close()
    o.close()

files = ["../ftrl_1","../ftrl_2","../fm_test_2.out","../fm_test_2_split"]
weights = [1,1,1,1]
ensemble(weights,files,"../ensemble")
sub("../ensemble","../test","../ensemble_sub")
calibrate("../ensemble_sub","../ensemble_cal")

