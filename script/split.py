import math
import sys

def load_result(result):
    fr = open(result)
    r = []
    y = []
    while True:
        line1 = fr.readline()
        if not line1 :
            break        
        r.append(float(line1))
    fr.close()
    return r


def merge(output,input1,input2):
    r1 = load_result(input1)
    r2 = load_result(input2)
    ori_file = "../test_pre"
    index = 1
       
    f = open(ori_file)
    sub = open(output,"w")
    line = f.readline()
 
    cnt1 = -1
    cnt2 = -1
    while True:
        line = f.readline()
        if not line:
            break
        fields = line.split(",")
        if fields[index+3]=="c_85f751fd":
            cnt2 += 1
            print >> sub, str(r2[cnt2])
        else:
            cnt1 += 1
            print >> sub, str(r1[cnt1])
    f.close()


merge(sys.argv[1],sys.argv[2],sys.argv[3])
