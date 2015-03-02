
def get_feature_num(train,max_num):
    f = open(train)
    num = max_num
    while True:
        line = f.readline()
        if not line:
            break
        ss = line.split(" ")
        for i in xrange(1,len(ss)):
            if num < int(ss[i]):
                num = int(ss[i])
    f.close()
    return num

def append(input,gbdt,output,num):
    f1 = open(input)
    f2 = open(gbdt)
    fo = open(output,"w")
    while True:
        line1 = f1.readline().strip()
        line2 = f2.readline().strip()
        if not line1:
            break
        gbdt_fea = []
        ss = line2.split(" ")
        for i in xrange(1,len(ss)):
            fea = str(i) + "_" + ss[i]
            idx = d.get(fea)
            if idx == None:
                d[fea] = num + 1 + len(d)
            gbdt_fea.append(str(d[fea]))
        print >> fo, line1+" "+" ".join(gbdt_fea)
    f1.close()
    f2.close()
    fo.close()

num = -1

input_train = "../fm_train_1"
input_test = "../fm_test_1"

gbdt_train = "../train_gbdt_out"
gbdt_test = "../test_gbdt_out"

output_train = "../fm_train_2"
output_test = "../fm_test_2"
num = get_feature_num(input_train,num)
num = get_feature_num(input_test,num)

d = {}

append(input_train,gbdt_train,output_train,num)
append(input_test,gbdt_test,output_test,num)
