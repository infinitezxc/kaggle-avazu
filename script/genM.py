import marshal
from math import log

site_null = "85f751fd"
app_null = "ecad2386"

[dic,dc] = marshal.load(open("../ip_dict"))
l = [""] * len(dic)
for x in dic:
    l[dic[x]] = x
for i in xrange(len(dc)):
    print dc[l[i]]
d = {}
fset = marshal.load(open("../fc"))

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
    if ip not in d:
        d[ip] = [0.] * len(dic)
    d[ip][dic[w]] += 1
    
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
    if ip not in d:
        d[ip] = [0.] * len(dic)
    d[ip][dic[w]] += 1
ll = float(len(d))
for k in d:
    s = reduce(lambda x,y:x + y,d[k])
    for i in xrange(len(d[k])):
        d[k][i] = d[k][i] / s * log(ll / dc[l[i]])

marshal.dump(d,open("../ip_mat","w"))