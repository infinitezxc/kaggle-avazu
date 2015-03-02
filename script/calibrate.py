import math
from pprint import pprint

train_ctr = 0.162

def get_pred_ctr(input_file):
    f = open(input_file)
    line = f.readline()
    cur_obj_idx = 0
    obj_ctr = 0
    obj_cnt = 0
    while True:
        line = f.readline()
        if line.strip()=='':
            break
        obj_cnt = obj_cnt + 1
        obj_ctr = obj_ctr + float(line.split(',')[1])
    print obj_cnt
    print obj_ctr/obj_cnt
    pred_ctr = (obj_ctr/obj_cnt)
    f.close()
    return pred_ctr

def inverse_logit(y):
    return math.log(y/(1-y))

def logit(x):
    return 1/(1+math.exp(-x))
    
def calibrate(input_file,output_file):
    # delta intercept
    pred_ctr = get_pred_ctr(input_file)
    intercept = (pred_ctr*(1-train_ctr)/train_ctr/(1-pred_ctr))

    f1 = open(input_file)
    f2 = open(output_file,'w')
    line = f1.readline()
    f2.write(line)
    cur_obj_idx = 0
    cnt = 0
    new_ctr = 0.0
    while True:
        cnt += 1
        line = f1.readline()
        if line.strip()=='':
            break
        fields = line.split(',')
        cur_ctr = float(fields[1])
        cal_ctr = logit(inverse_logit(cur_ctr)-math.log(intercept))
        new_ctr += cal_ctr
        f2.write(fields[0]+","+str(cal_ctr)+"\n")
    f1.close()
    f2.close()
    print new_ctr/cnt

