f1 = open("../train_pre_1")
f2 = open("../test_pre_1")
out1 = open("../train_pre_1b","w")
out2 = open("../test_pre_1b","w")
t = open("../train_gbdt_out")
v = open("../test_gbdt_out")
add = []
for i in xrange(30,49):
	add.append("C" + str(i))

line = f1.readline()
print >> out1, line[:-1] + "," + ",".join(add)
line = f2.readline()
print >> out2, line[:-1] + "," + ",".join(add)
for i in xrange(40428967):
	line = f1.readline()[:-1]
	a = t.readline()[:-1]
	ll = a.split(" ")[1:]
	for j in xrange(19):
		line += "," + add[j] + "_" + ll[j]
	print >> out1,line
for i in xrange(4577464):
	line = f2.readline()[:-1]
	a = v.readline()[:-1]
	ll = a.split(" ")[1:]
	for j in xrange(19):
		line += "," + add[j] + "_" + ll[j]
	print >> out2,line

f1.close()
f2.close()
out1.close()
out2.close()
t.close()
v.close()
