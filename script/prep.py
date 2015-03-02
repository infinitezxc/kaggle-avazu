import marshal

ftr = "../train_c"
fte = "../test_c"
fset = marshal.load(open("../fc"))
rare_d = marshal.load(open("../rare_d"))
ftrain = "../train_pre"
ftest = "../test_pre"

id_day = marshal.load(open("../id_day"))

def prep(input,output,isTest):
    f = open(input)
    out = open(output,"w")
    line = f.readline()
    print >> out,line[:-1]
    count = 0
    bias = 3
    if isTest:
        bias = 2
    while True:
        line = f.readline()
        if not line:
            break
        count += 1
        if count % 100000 == 0:
            print count
        lis = line[:-1].split(",")
        uid = "??"
        for i in xrange(bias,len(lis)):
            name = chr(ord('a') + i - bias)
            if name == "j":
                ip = name + "_" + lis[i]
                rare = rare_d.get(ip)
                if rare != None:
                    lis[i] = "j_rare_" + str(rare)
                    #print lis[i]
                    continue
            if name == "i":
                id = name + "_" + lis[i]
                rare = rare_d.get(id)
                if rare != None:
                    lis[i] = "i_rare_" + str(rare)
                    #print lis[i]
                    continue
            if name == "v":
                id = name + "_" + lis[i]
                uid = id
                rare = rare_d.get(id)
                if rare != None:
                    lis[i] = "v_rare_" + str(rare)
                    continue
                elif id_day.get(id) == 1:
                    lis[i] = "v_id_s"
                    continue
            if name + "_" + lis[i] not in fset and i < len(lis) - 6:
                lis[i] = name + "_rare"
            else:
                lis[i] = name + "_" + lis[i]
        lis.append("id_day_"+str(id_day[uid]))
        print >> out,",".join(lis)
    f.close()
    out.close()

prep(ftr,ftrain,False)
prep(fte,ftest,True)