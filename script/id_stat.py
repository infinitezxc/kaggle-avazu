import marshal
 
def stat(input):
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
        # identical id
        index = len(lis)-7
        iid = "v_"+lis[index]
        if iid in d_id:
            d_id[iid] += 1
        else:
            d_id[iid] = 1
        # ip
        index = len(lis)-19
        ip = "j_"+lis[index]
        if ip in d_id:
            d_id[ip] += 1
        else:
            d_id[ip] = 1
        # id
        index = len(lis)-20
        id = "i_"+lis[index]
        if id in d_id:
            d_id[id] += 1
        else:
            d_id[id] = 1
    f.close()

d_id = {}

stat("../train_c")
stat("../test_c")


marshal.dump(d_id,open("../id_stat","w"))