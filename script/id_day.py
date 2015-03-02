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
        # ip
        index = 12
        if isTest:
            index = 11
        ip = "j_" + lis[index]
        if ip in d_id:
            d_id[ip].add(lis[2][4:6])
        else:
            s = set()
            s.add(lis[2][4:6])
            d_id[ip] = s
        # identical id
        index = len(lis)-7
        iid = "v_"+lis[index]
        if iid in d_id:
            d_id[iid].add(lis[2][4:6])
        else:
            s = set()
            s.add(lis[2][4:6])
            d_id[iid] = s
    f.close()

d_id = {}
d_set = {}

stat("../train_c",False)
stat("../test_c",True)

for k in d_id:
    d_set[k] = len(d_id[k])

marshal.dump(d_set,open("../id_day","w"))
