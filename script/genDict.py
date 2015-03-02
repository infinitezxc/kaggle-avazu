import marshal

d = {}
dc = {}
l = []
fset = marshal.load(open("../fc"))
site_null = "85f751fd"
app_null = "ecad2386"

f1 = open("../train_c")
f2 = open("../test_c")
line = f1.readline()
line = f2.readline()
count = 0
while True:
    line = f1.readline()
    if not line:
        break
    count += 1
    if count % 100000 == 0:
        print count
    lis = line[:-1].split(",")
    date = int(lis[2][4:6])
    ip = lis[12]
    if "j_" + ip not in fset:
        continue
    w = lis[7]
    if lis[5] == site_null:
        w = lis[10]
    if w not in dc:
        dc[w] = set()
        dc[w].add(ip)
    else:
        dc[w].add(ip)
    if w not in d:
        l.append(w)
        d[w] = len(l) - 1
    
count = 0
while True:
    line = f2.readline()
    if not line:
        break
    count += 1
    if count % 100000 == 0:
        print count
    lis = line[:-1].split(",")
    ip = lis[11]
    if "j_" + ip not in fset:
        continue
    w = lis[6]
    if lis[4] == site_null:
        w = lis[9]
    if w not in dc:
        dc[w] = set()
        dc[w].add(ip)
    else:
        dc[w].add(ip)
    if w not in d:
        l.append(w)
        d[w] = len(l) - 1
print len(d)
for k in dc:
    dc[k] = len(dc[k])
marshal.dump([d,dc],open("../ip_dict","w"))