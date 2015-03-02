import marshal
 
def stat(input,isTest):
    f = open(input)
    line = f.readline()
    count = 0
    while True:
        line = f.readline()
        if not line:
            break
        count += 1
        if count % 100000 == 0:
            print count
        lis = line.split(",")
        index = 11
        if isTest:
            index = 10
        id = "i_"+lis[index]
        ip = "j_" + lis[index+1]
        iid = "v_" + lis[len(lis)-7]
        if id in d:
            d[id] += 1
        else:
            d[id] = 1
        if ip in d:
            d[ip] += 1
        else:
            d[ip] = 1
        if iid in d:
            d[iid] += 1
        else:
            d[iid] = 1
    f.close()

d = {}

stat("../train_c",False)
stat("../test_c",True)

rare_d = {}

for k in d:
    if d[k] <=10:
        rare_d[k] = d[k]

marshal.dump(rare_d,open("../rare_d","w"))