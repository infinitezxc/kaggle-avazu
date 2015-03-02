'''
           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                   Version 2, December 2004

Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.

           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

 0. You just DO WHAT THE FUCK YOU WANT TO.
'''


from datetime import datetime
from csv import DictReader
from math import exp, log, sqrt
import marshal


# TL; DR, the main training process starts on line: 250,
# you may want to start reading the code from there


##############################################################################
# parameters #################################################################
##############################################################################

# A, paths
train = '../train_pre_1b'               # path to training file
test = '../test_pre_1b'                 # path to testing file
submission = '../ftrl_2'  # path of to be outputted submission file

# B, model
alpha = .05  # learning rate
beta = 1.   # smoothing parameter for adaptive learning rate
L1 = .4     # L1 regularization, larger value means more regularized
L2 = .1     # L2 regularization, larger value means more regularized

# C, feature/hash trick
D = 2 ** 26            # number of weights to use
interaction = True     # whether to enable poly2 feature interactions
SUB = True

# D, training/validation
epoch = 3       # learn training data for N passes
holdafter = 30 if SUB else 28 # data after date N (exclusive) are used as validation
holdout = None  # use every N training instance for holdout validation

#interactions
inter_s = "ac,bc,bi,bk,ci,ck,cm,cn,in,jc,cw,tc,xc,yc,zc,1c,2c,3c,4c,x1,x2,x3,x4,xy,xz" #site
inter = []
inter_s2 = "af,bf,bi,bk,fi,fk,fm,fn,in,jf,fw,tf,xf,yf,zf,1f,2f,3f,4f,x1,x2,x3,x4,xy,xz" #app
inter2 = []
featdict = {"a":"C1","b":"banner_pos","c":"site_id","d":"site_domain","e":"site_category","f":"app_id","g":"app_domain","h":"app_category","i":"device_id","j":"ips","k":"device_model","l":"device_type","m":"device_conn_type","n":"C14","o":"C15","p":"C16","q":"C17","r":"C18","s":"C19","t":"C20","u":"C21","w":"ipcate","x":"C22","y":"C23","z":"C24","1":"C25","2":"C26","3":"C27","4":"C28"}
for i in inter_s.split(","):
    inter.append((featdict[i[0]],featdict[i[1]]))
for i in inter_s2.split(","):
    inter2.append((featdict[i[0]],featdict[i[1]]))
for i in xrange(29,49):
	co = "C" + str(i)
	inter.append((co,"site_id"))
	inter2.append((co,"app_id"))
ipcate = marshal.load(open("../testcate"))

def convt(s,t):
    s = s.split("_")[1]
    if int(s) <= 70:
        return t + "_" + s
    else:
        return t + "_" + "l"

##############################################################################
# class, function, generator definitions #####################################
##############################################################################

class ftrl_proximal(object):
    ''' Our main algorithm: Follow the regularized leader - proximal

        In short,
        this is an adaptive-learning-rate sparse logistic-regression with
        efficient L1-L2-regularization

        Reference:
        http://www.eecs.tufts.edu/~dsculley/papers/ad-click-prediction.pdf
    '''

    def __init__(self, alpha, beta, L1, L2, D, interaction):
        # parameters
        self.alpha = alpha
        self.beta = beta
        self.L1 = L1
        self.L2 = L2

        # feature related parameters
        self.D = D
        self.interaction = interaction

        # model
        # n: squared sum of past gradients
        # z: weights
        # w: lazy weights
        self.n = [0.] * D
        self.z = [0.] * D
        self.w = [0.] * D

    def _indices(self, x):
        ''' A helper generator that yields the indices in x

            The purpose of this generator is to make the following
            code a bit cleaner when doing feature interaction.
        '''

        # first yield index of the bias term
        yield 0

        D = self.D
        # then yield the normal indices
        for feat in x:
            index = abs(hash(feat)) % D
            yield index

    def predict(self, x):
        ''' Get probability estimation on x

            INPUT:
                x: features

            OUTPUT:
                probability of p(y = 1 | x; w)
        '''

        # model
        w = self.w

        # wTx is the inner product of w and x
        wTx = 0.
        for i in self._indices(x):
            wTx += w[i]

        # bounded sigmoid function, this is the probability estimation
        return 1. / (1. + exp(-max(min(wTx, 35.), -35.)))

    def update(self, x, p, y):
        ''' Update model using x, p, y

            INPUT:
                x: feature, a list of indices
                p: click probability prediction of our model
                y: answer

            MODIFIES:
                self.n: increase by squared gradient
                self.z: weights
        '''

        # parameter
        alpha = self.alpha

        # model
        n = self.n
        z = self.z
        w = self.w

        # gradient under logloss
        g = p - y

        # update z and n
        tmp = 0
        for i in self._indices(x):
            sigma = (sqrt(n[i] + g * g) - sqrt(n[i])) / alpha
            z[i] += g - sigma * w[i]
            n[i] += g * g
            sign = -1. if z[i] < 0 else 1.  # get sign of z[i]
            # build w using z and n
            if sign * z[i] <= L1:
                # w[i] vanishes due to L1 regularization
                w[i] = 0.
            else:
                # apply prediction time L1, L2 regularization to z and get w
                w[i] = (sign * L1 - z[i]) / ((beta + sqrt(n[i])) / alpha + L2)

def logloss(p, y):
    ''' FUNCTION: Bounded logloss

        INPUT:
            p: our prediction
            y: real answer

        OUTPUT:
            logarithmic loss of p given y
    '''

    p = max(min(p, 1. - 10e-15), 10e-15)
    return -log(p) if y == 1. else -log(1. - p)


def data(path, D):
    ''' GENERATOR: Robotly hash-trick to the original csv row
                   and for simplicity, we one-hot-encode everything

        INPUT:
            path: path to training or testing file
            D: the max index that we can hash to

        YIELDS:
            ID: id of the instance, mainly useless
            x: a list of hashed and one-hot-encoded 'indices'
               we only need the index since all values are either 0 or 1
            y: y = 1 if we have a click, else we have y = 0
    '''

    for t, row in enumerate(DictReader(open(path))):
        # process id
        ID = row['id']
        del row['id']

        # process clicks
        y = 0.
        if 'click' in row:
            if row['click'] == '1':
                y = 1.
            del row['click']

        # extract date
        date = int(row['hour'][4:6])
        row["C28"] = convt(row["C28"],"C28")
        del row["hour"]
        row["ips"] = row["device_ip"]
        if row["device_ip"][-3:] == "ips":
            row["device_ip"] = "ips"
            row["ips"] = row["ips"][:-3]
        row["ipcate"] = "ipcate_null"
        if row["ips"][2:] in ipcate:
            row["ipcate"] = "ipcate_" + str(ipcate[row["ips"][2:]])
        # turn hour really into hour, it was originally YYMMDDHH
        isApp = row["site_id"] == "c_85f751fd" 
        if isApp:
            del row["site_id"]
            del row["site_domain"]
            del row["site_category"]
        else:
            del row["app_id"]
            del row["app_domain"]
            del row["app_category"]
        # build x
        x = []
        if interaction:
            if not isApp:
                for pair in inter:
                    x.append(row[pair[0]] + "_" + row[pair[1]])
            else:
                for pair in inter2:
                    x.append(row[pair[0]] + "_" + row[pair[1]])
        del row["ips"]
        for key in row:
            value = row[key]
            # one-hot encode everything with hash trick
            x.append(value)

        yield t, date, ID, x, y, isApp


##############################################################################
# start training #############################################################
##############################################################################

start = datetime.now()

# initialize ourselves a learner
learner1 = ftrl_proximal(alpha, beta, L1, L2, D, interaction)
learner2 = ftrl_proximal(alpha, beta, L1, L2, D, interaction)

# start training
for e in xrange(epoch):
    loss1 = 0.
    loss2 = 0.
    count1 = 1
    count2 = 1
    loss = 0.
    count = 1
    localcount = 0
    learner1.alpha = 0.05 - 0.01 * e
    learner2.alpha = 0.05 - 0.01 * e
    for t, date, ID, x, y, isApp in data(train, D):  # data is a generator
        #    t: just a instance counter
        # date: you know what this is
        #   ID: id provided in original data
        #    x: features
        #    y: label (click)

        # step 1, get prediction from learner
        if not isApp:
            p = learner1.predict(x)
        else:
            p = learner2.predict(x)
        
        #print progress
        localcount += 1
        if localcount % 1000000 == 0:
            if (holdafter and date > holdafter) or (holdout and t % holdout == 0):
                print "valid: " + str(localcount)
            else:
                print "train: " + str(localcount)

        if (holdafter and date > holdafter) or (holdout and t % holdout == 0):
            # step 2-1, calculate validation loss
            #           we do not train with the validation data so that our
            #           validation loss is an accurate estimation
            #
            # holdafter: train instances from day 1 to day N
            #            validate with instances from day N + 1 and after
            #
            # holdout: validate with every N instance, train with others
            loss += logloss(p,y)
            count += 1
            if isApp:
                loss1 += logloss(p, y)
                count1 += 1
            else:
                loss2 += logloss(p, y)
                count2 += 1
        else:
            # step 2-2, update learner with label (click) information
            if not isApp:
                learner1.update(x, p, y)
            else:
                learner2.update(x, p, y)
    if not SUB:
        print('Epoch %d finished, validation logloss: %f, logloss1: %f, logloss2: %f, elapsed time: %s' % (e, loss/count, loss1/count1, loss2/count2, str(datetime.now() - start)))

##############################################################################
# start testing, and build Kaggle's submission file ##########################
##############################################################################
def sub():
    with open(submission, 'w') as outfile:
        for t, date, ID, x, y, isApp in data(test, D):
            if not isApp:
                p = learner1.predict(x)
            else:
                p = learner2.predict(x)
            outfile.write('%f\n' % p)

sub()